from humanoid.locomotion.lipm_dynamics import LIPMDynamics

def test_step():

    lipm=LIPMDynamics()

    x,v=lipm.step(0,0.2,0.02)

    assert isinstance(x,float)