from PetriDish import PetriDish

def run():

    ptA = PetriDish(save_interval=100) 
    #ptA = PetriDish()
    ptA.run()

if __name__ == "__main__":
    run()
