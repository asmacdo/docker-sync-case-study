from stages import HelloStage, PrintStage, run_pipeline


def hello_world_demo():
    """
    Here, we use create 2 simple stages, and show that they work together.
    """
    # pass "hello" and "world" into out_q.
    heya = HelloStage()
    print_stuff = PrintStage()
    stages = [heya, print_stuff]
    run_pipeline(stages)


hello_world_demo()
