from stages import PrintStage, PrintAndPassStage, ConcurrentRunner, run_pipeline, StageGroup

from mock_docker import DockerStart, DownloadContent, ProcessContent, SaveContent, ContentRelations


def docker_manymany_problem():
    print("We have another step, and it presents a problem. Each of these content types"
          " are related to each other. To make matters more difficult, they have"
          " many-to-many relationships. This is a problem for our current setup because"
          " each item streams through individually.")
    print()
    print()
    print("To demo the problem, I've written a mock many-to-many that is used by the "
          "ContentRelations Stage. All it does is let us know if both of the objects we "
          "are trying to fake relate have already been fake saved to the db.")
    print("Sometimes, we will get lucky and objects just happen to pass through in the right "
          "order, but most of the many-to-many writes will fail.")
    make_content = DockerStart(blobs=1, manifests=1, manifest_lists=1)
    download_content = ConcurrentRunner(DownloadContent())
    process = ProcessContent()
    save_stage = SaveContent()
    handle_content = StageGroup([download_content, process, save_stage])
    relate_content = ContentRelations()
    print_end = PrintStage()
    stages = [make_content, handle_content, handle_content, handle_content,
              relate_content, print_end]
    run_pipeline(stages)


docker_manymany_problem()
