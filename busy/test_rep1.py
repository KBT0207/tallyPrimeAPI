import psutil
import pytest
from busy.busy_utils import is_process_running

# Define fixtures if necessary
@pytest.fixture
def mock_process_iter(monkeypatch):
    def mock_iter():
        return [
            psutil.Process(pid=100, name='Process1'),
            psutil.Process(pid=101, name='Process2'),
            psutil.Process(pid=102, name='Process3')
        ]
    monkeypatch.setattr(psutil, 'process_iter', mock_iter)

# Test cases
def test_process_running(mock_process_iter):
    assert is_process_running("Process2") == True

def test_process_not_running(mock_process_iter):
    assert is_process_running("NonexistentProcess") == False

def test_process_running_multiple(mock_process_iter):
    assert is_process_running("Process1") == True

def test_process_not_running_empty_list(monkeypatch):
    def mock_iter():
        return []
    monkeypatch.setattr(psutil, 'process_iter', mock_iter)
    assert is_process_running("NonexistentProcess") == False
