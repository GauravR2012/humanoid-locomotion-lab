import numpy as np
from scipy.linalg import solve_discrete_are


class ZMPPreviewController:

    def __init__(self, dt=0.01, com_height=0.35, preview_time=1.6, g=9.81):

        self.dt = dt
        self.h = com_height
        self.g = g
        self.N = int(preview_time / dt)

        self.A = np.array([
            [1, dt, dt**2/2],
            [0, 1, dt],
            [0, 0, 1]
        ])

        self.B = np.array([
            [dt**3/6],
            [dt**2/2],
            [dt]
        ])

        self.C = np.array([[1, 0, -self.h/self.g]])

        A_bar = np.block([
            [1, -self.C @ self.A],
            [np.zeros((3,1)), self.A]
        ])

        B_bar = np.vstack((-self.C @ self.B, self.B))

        Q = np.diag([1,0,0,0])
        R = np.array([[1e-6]])

        P = solve_discrete_are(A_bar, B_bar, Q, R)

        K = np.linalg.inv(B_bar.T @ P @ B_bar + R) @ (B_bar.T @ P @ A_bar)

        self.Ki = K[0,0]
        self.Kx = K[0,1:]

        self.G = []

        X = -(A_bar - B_bar @ K).T @ P @ np.array([[1],[0],[0],[0]])

        for i in range(self.N):

            self.G.append(
                (np.linalg.inv(B_bar.T @ P @ B_bar + R)
                @ B_bar.T @ X)[0,0]
            )

            X = (A_bar - B_bar @ K).T @ X

        self.G = np.array(self.G)

        self.x = np.zeros((3,1))
        self.e = 0


    def step(self, zmp_ref):

        preview = zmp_ref[:self.N]

        u = -self.Ki * self.e - self.Kx @ self.x.flatten()

        for i in range(len(preview)):
            u -= self.G[i] * preview[i]

        u = float(u)

        self.x = self.A @ self.x + self.B * u

        zmp = (self.C @ self.x)[0,0]

        self.e += zmp - zmp_ref[0]

        return self.x[0,0], self.x[1,0], zmp