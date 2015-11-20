from persispy.phc.interface import phc_cloud

def main():
    phc_cloud(eqn = "x^2 - y",DEBUG=True)
    phc_cloud(eqn = "x^2 + y^2 - 1",DEBUG=True)
    phc_cloud(eqn = "x^2 + y^3 - 1",DEBUG=True)
    phc_cloud(eqn = "x^2 + y^2 + z^2 - 1",DEBUG=True)
    phc_cloud(eqn = "x^2 + y^2 + z^2 + a - 1",DEBUG=True)

if __name__== "__main__": main()

