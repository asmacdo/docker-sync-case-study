from stages import (PrintStage, PrintAndPassStage, ConcurrentRunner, run_pipeline, StageGroup,
                    WaitUntilComplete)

from mock_docker import DockerStart, DownloadContent, ProcessContent, SaveContent, ContentRelations


def docker_manymany_solution():
    print("So, how can we ensure that all the models are saved before we try to write "
          "a many-to-many relationship?")
    print("Let's start with the easy way, but it's not ideal.")
    print("Just add a new custom Stage, WaitUntilComplete.")
    print("Now, all the writes should work.")
    make_content = DockerStart(blobs=1, manifests=1, manifest_lists=1)
    download_content = ConcurrentRunner(DownloadContent())
    process = ProcessContent()
    save_stage = SaveContent()
    handle_content = StageGroup([download_content, process, save_stage])
    wait_stage = WaitUntilComplete()
    relate_content = ContentRelations()
    print_end = PrintStage()
    stages = [make_content, handle_content, handle_content, handle_content,
              wait_stage, relate_content, print_end]
    run_pipeline(stages)
    print("... Unfortunately, every single content stayed in memory until the whole task "
          "completed. This pattern limits works against good asynchronous design.")


docker_manymany_solution()
