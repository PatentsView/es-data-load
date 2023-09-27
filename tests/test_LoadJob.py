from es_data_load.specification import LoadConfiguration
from tests.test_es import assert_es_counts


def test_generate_load_job_from_folder(project_root, config):
    test_mapping_folder = "tests/patent_citations_loads"
    full_test_mapping_path = "{root}/{relative_folder_path}".format(
            relative_folder_path=test_mapping_folder,
            root=project_root)
    lj = LoadConfiguration.generate_load_configuration_from_folder(full_test_mapping_path)
    assert len(lj.get_load_operation_names()) == 1
    test_mapping_folder = "tests/all_citations_loads"
    full_test_mapping_path = "{root}/{relative_folder_path}".format(
            relative_folder_path=test_mapping_folder,
            root=project_root)

    lj = LoadConfiguration.generate_load_configuration_from_folder(full_test_mapping_path)
    assert len(lj.get_load_operation_names()) == 2


def test_add_load_operation(project_root, config):
    assert False


def test_get_load_operation_names(load_job_2):
    ljns = load_job_2.get_load_operation_names()
    assert all([x in ['patent_citation', 'application_citation'] for x in ljns]) and all(
            [x in ljns for x in ['patent_citation', 'application_citation']])


def test_process_load_operation(load_job_1: LoadConfiguration):
    load_job_1.searchtarget.es.indices.delete(
            index=load_job_1.get_load_job_status('patent_citation')['target_setting']['index'])
    load_job_1.process_load_operation('patent_citation')
    assert_es_counts(
            load_job_1.searchtarget,
            load_job_1.get_load_job_status('patent_citation')['target_setting'])


def test_process_all_load_operations(project_root, config):
    assert False


def test_get_load_job_status(load_job_1):
    load_job_1.searchtarget.es.indices.delete(
            index=load_job_1.get_load_job_status('patent_citation')['target_setting']['index'])
    load_job_1.process_load_operation('patent_citation')
    status = load_job_1.get_load_job_status('patent_citation')
    assert all(x in status.keys() for x in ['batches', 'record_count', 'complete', 'success', 'duration'])
    assert status['complete'] and ['success']
