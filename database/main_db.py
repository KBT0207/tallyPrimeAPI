import glob
import pandas as pd
import os
from datetime import datetime, timedelta
from database.sql_connector import kbbio_engine, kbbio_connector, kbe_connector, kbe_engine
from database.busy_data_processor import BusyDataProcessor, get_filename, get_compname
from database.tally_data_processor import get_compname_tally,get_date_tally,get_filename_tally
from database.tally_data_processor import TallyDataProcessor
from database.models.base import KBBIOBase, KBEBase
from database.db_crud import DatabaseCrud
from logging_config import logger
from utils.common_utils import tally_tables,report_table_map, mc_map
from utils.email import email_send
import requests
from sqlalchemy.exc import SQLAlchemyError
import os, glob



def import_tally_data(date):
    KBEBase.metadata.create_all(kbe_engine)
    
    tally_files = glob.glob(f"E:\\api_download\\**\\*{date}*.json", recursive=True)

    if len(tally_files) != 0:
        for file in tally_files:
            json_data = TallyDataProcessor(file)
            importer = DatabaseCrud(kbe_connector)
                
            if get_filename_tally(file) == 'sales':
                importer.import_data("tally_sales_detailed",json_data.clean_and_transform(),commit=True)

            if get_filename_tally(file) == 'sales-return':
                importer.import_data("tally_sales_return_detailed",json_data.clean_and_transform(),commit=True)

            if get_filename_tally(file) == 'purchase':
                importer.import_data("tally_purchase_detailed",json_data.clean_and_transform(),commit=True)

            if get_filename_tally(file) == 'purchase-return':
                importer.import_data("tally_purchase_return_detailed",json_data.clean_and_transform(),commit=True)

            if get_filename_tally(file) == 'item':
                importer.import_data("tally_items",json_data.clean_and_transform(),commit=True)

            if get_filename_tally(file) == 'master':
                importer.import_data("tally_masters",json_data.clean_and_transform(),commit=True)

                logger.info(f"{get_filename_tally(file)} and {get_compname(file)} imported into database.. ")

    else:
        logger.critical("No File for today's date found to import in database")


def delete_tally_data_file_wise(start_date: str, end_date: str, file_date: str, commit: bool):

    KBEBase.metadata.create_all(kbe_engine)
    
    tally_files = glob.glob(f"E:\\api_download\\**\\*{file_date}*.json", recursive=True)

    if not tally_files:
        logger.info(f"No files found for file date: {file_date}")
        return

    delete_tally_data_mc_wise = DatabaseCrud(kbe_connector)

    for file_path in tally_files:
        try:
            file_name = os.path.basename(file_path)

            mc = get_compname_tally(file_path).replace("_", " ")
            if mc == 'Unknown Company':
                logger.info(f"Skipping file '{file_name}' because material centre is Unknown Company.")
                continue

            report_type = get_filename_tally(file_path).lower()
            table_name = report_table_map.get(report_type)

            if not table_name:
                logger.warning(f"Unknown report type '{report_type}' in file '{file_name}', skipping.")
                continue

            logger.info(f"Deleting data from table '{table_name}' for material centre '{mc}' based on file '{file_name}'.")

            if table_name in ['tally_masters', 'tally_items']:
                delete_tally_data_mc_wise.delete_tally_material_centre_and_datewise(
                    table_name=table_name,
                    start_date=None,
                    end_date=None,
                    material_centre=[mc],
                    commit=commit
                )
            else:
                delete_tally_data_mc_wise.delete_tally_material_centre_and_datewise(
                    table_name=table_name,
                    start_date=start_date,
                    end_date=end_date,
                    material_centre=[mc],
                    commit=commit
                )

        except Exception as e:
            logger.error(f"Error processing file '{file_path}': {e}")
            continue



def delete_tally_data_comp(start_date: str, end_date: str, file_date: str, commit: bool):
    KBEBase.metadata.create_all(kbe_engine)

    tally_files = glob.glob(f"E:\\api_download\\**\\*{file_date}*.json", recursive=True)

    if not tally_files:
        logger.info(f"No files found for file date: {file_date}")
        return

    delete_tally_data_mc_wise = DatabaseCrud(kbe_connector)

    for file_path in tally_files:
        try:
            file_name = os.path.basename(file_path)
            mc_key = get_compname_tally(file_path).replace("_", " ")

            mc_data = mc_map.get(mc_key)
            if not mc_data:
                logger.warning(f"Company '{mc_key}' not found in mc_map.")
                continue

            mc = mc_data[0]
            comp_start_date, comp_end_date = mc_data[1:3]

            if mc == 'Unknown Company':
                logger.info(f"Skipping file '{file_name}' because material centre is Unknown Company.")
                continue

            input_start = datetime.strptime(start_date, "%Y-%m-%d").date()
            input_end = datetime.strptime(end_date, "%Y-%m-%d").date()
            comp_start = datetime.strptime(comp_start_date, "%Y-%m-%d").date()
            comp_end = datetime.strptime(comp_end_date, "%Y-%m-%d").date()

            if input_start < comp_start or input_end > comp_end:
                logger.info(
                    f"Skipping deletion for '{mc}' from file '{file_name}': "
                    f"input range [{input_start} to {input_end}] not within "
                    f"company range [{comp_start} to {comp_end}]."
                )
                continue

            report_type = get_filename_tally(file_path).lower()
            table_name = report_table_map.get(report_type)

            if not table_name:
                logger.warning(f"Unknown report type '{report_type}' in file '{file_name}', skipping.")
                continue

            logger.info(
                f"Deleting data from table '{table_name}' for material centre '{mc}' "
                f"between {start_date} and {end_date}."
            )

            if table_name in ['tally_masters', 'tally_items']:
                delete_tally_data_mc_wise.delete_tally_material_centre_and_datewise(
                    table_name=table_name,
                    start_date=start_date,
                    end_date=end_date,
                    material_centre=[mc],
                    commit=commit
                )
            else:
                delete_tally_data_mc_wise.delete_tally_material_centre_and_datewise(
                    table_name=table_name,
                    start_date=start_date,
                    end_date=end_date,
                    material_centre=[mc],
                    commit=commit
                )

        except Exception as e:
            logger.error(f"Error processing file '{file_path}': {e}")
            continue
