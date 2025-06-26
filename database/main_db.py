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
from utils.common_utils import tally_tables,report_table_map,kb_daily_exported_data
from utils.email import email_send
import requests
from sqlalchemy.exc import SQLAlchemyError
import os, glob



def import_tally_data(date):
    KBEBase.metadata.create_all(kbe_engine)
    tally_files = glob.glob(f"E:\\api_download\\**\\*{date}*.json", recursive=True)

    if tally_files:
        for file in tally_files:
            try:
                json_data = TallyDataProcessor(file)
                importer = DatabaseCrud(kbe_connector)
                file_type = get_filename_tally(file)
                if file_type in report_table_map:
                    table_name = report_table_map[file_type]
                    importer.import_data(table_name, json_data.clean_and_transform(), commit=True)
                    logger.info(f"Successfully imported {file} into {table_name}")
                else:
                    logger.warning(f"Unrecognized file type {file_type} in {file}")

            except Exception as e:
                logger.error(f"Error processing file {file}: {e}")

    else:
        logger.critical("No files for today's date found to import into the database.")

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


