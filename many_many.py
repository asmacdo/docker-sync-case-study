class MockManyMany:
    def write(model1, model2):
        if model1.saved and model2.saved:
            print("Success: through-table fake write")
        else:
            print("****Failed****: Both models are not saved.")
