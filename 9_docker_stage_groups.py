from stages import PrintStage, PrintAndPassStage, ConcurrentRunner, run_pipeline, StageGroup

from mock_docker import DockerStart, DownloadContent, ProcessContent, SaveContent


def docker_grouped_dps():
    print("Can that be simpler? Yup, let's group the repeated stage into a group.")
    print("The results should be exactly the same, though possibly in a different order.")
    make_content = DockerStart(blobs=1, manifests=1, manifest_lists=1)
    download_content = ConcurrentRunner(DownloadContent())
    process = ProcessContent()
    save_stage = SaveContent()
    handle_content = StageGroup([download_content, process, save_stage])
    print_end = PrintStage()
    stages = [make_content, handle_content, handle_content, handle_content, print_end]
    run_pipeline(stages)
    print("If you thought 'Why not just loop?', I had the same thought. See `apx_1_loops.py`.")


docker_grouped_dps()
