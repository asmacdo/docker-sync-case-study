from stages import HelloStage, PrintStage, StageGroup, WaitUntilComplete, run_pipeline


def stage_group_demo():
    """
    Stage groups are treated as Stages, and creates an inner pipeline of its own.
    """
    print("Stage Group demo.")
    print("Stage groups can help you to abstract groups that are used together.")
    heya = HelloStage(sleep=True)
    print_stuff = PrintStage()
    stages = [heya, print_stuff]
    stage_group = StageGroup(stages)
    run_pipeline([stage_group, stage_group])


def wait_demo():
    """
    """
    print("Wait demo.")
    print("Wait stages can make sure that tasks are ready to be executed.")
    print("Notice that the order is changed from the stage_group_demo.")
    heya = HelloStage(sleep=True)
    print_stuff = PrintStage()
    wait = WaitUntilComplete()
    stages = [heya, wait, print_stuff]
    stage_group = StageGroup(stages)
    run_pipeline([stage_group, stage_group])


stage_group_demo()
wait_demo()
