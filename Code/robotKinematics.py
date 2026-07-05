import math
import numpy as np

# Precomputed constants
SQRT3 = math.sqrt(3)

class RobotKinematics:
    def __init__(self, lp=79, l1=100, l2=80, lb=40, invert=False):
        self.lp = lp    # Radius of Top
        self.l1 = l1    # Top Arm
        self.l2 = l2    # Bottom Arm
        self.lb = lb    # Radius of Bottom
        self.invert = invert  # Whether the arm stays inward or outward

        self.maxh = self.compute_maxh() - 1
        self.minh = self.compute_minh() + 1
        self.p = [0.0, 0.0, self.maxh]
        self.h = (self.maxh + self.minh) / 2
        self.maxtheta = 10

        # Node coordinates
        self.A1 = [0, 0, 0]
        self.A2 = [0, 0, 0]
        self.A3 = [0, 0, 0]

        self.B1 = [0, 0, 0]
        self.B2 = [0, 0, 0]
        self.B3 = [0, 0, 0]

        self.C1 = [0.0, 0.0, 0.0]
        self.C2 = [0.0, 0.0, 0.0]
        self.C3 = [0.0, 0.0, 0.0]

        self.max_theta(self.h)

        self.theta1 = 0
        self.theta2 = 0
        self.theta3 = 0

    def compute_maxh(self):
        return math.sqrt((self.l1 + self.l2) ** 2 - (self.lp - self.lb) ** 2)

    def compute_minh(self):
        if self.l1 > self.l2:
            return math.sqrt(self.l1 ** 2 - (self.lb + self.l2 - self.lp) ** 2)
        elif self.l2 > self.l1:
            return math.sqrt((self.l2 - self.l1) ** 2 - (self.lp - self.lb) ** 2)
        else:
            return 0

    def solve_top(self, a, b, c, h):
        lp, sqrt3 = self.lp, SQRT3
        if not self.invert:
            denom1 = math.sqrt(4*c*c + (a - sqrt3*b)**2)
            denom2 = math.sqrt(c*c + a*a)
            denom3 = math.sqrt(4*c*c + (a + sqrt3*b)**2)

            self.A1 = [-(lp*c) / denom1,
                       (sqrt3*lp*c) / denom1,
                       h + ((a - sqrt3*b)*lp) / denom1]

            self.A2 = [(lp*c) / denom2,
                       0,
                       h - (lp*a) / denom2]

            self.A3 = [-(lp*c) / denom3,
                       -(sqrt3*lp*c) / denom3,
                       h + ((a + sqrt3*b)*lp) / denom3]
        else:
            # Same as above, could share code if invert logic changes later
            denom1 = math.sqrt(4*c*c + (a - sqrt3*b)**2)
            denom2 = math.sqrt(c*c + a*a)
            denom3 = math.sqrt(4*c*c + (a + sqrt3*b)**2)

            self.A1 = [-(lp*c) / denom1,
                       (sqrt3*lp*c) / denom1,
                       h + ((a - sqrt3*b)*lp) / denom1]

            self.A2 = [(lp*c) / denom2,
                       0,
                       h - (lp*a) / denom2]

            self.A3 = [-(lp*c) / denom3,
                       -(sqrt3*lp*c) / denom3,
                       h + ((a + sqrt3*b)*lp) / denom3]

    def solve_middle(self):
        lb, l1, l2, sqrt3 = self.lb, self.l1, self.l2, SQRT3
        a11, a12, a13 = self.A1
        a21, a22, a23 = self.A2
        a31, a32, a33 = self.A3

        # Common function for computing Ci
        def compute_C(p, q, invert=False):
            r = p*p + (4 if invert in (0, 2) else 1)
            s = 2*p*q + (4*lb if invert in (0, 2) else -2*lb)
            t = q*q + (lb*lb if invert in (0, 2) else lb*lb - l2*l2)
            return r, s, t

        # Precompute common expressions
        p1 = (-a11 + sqrt3*a12 - 2*lb) / a13
        q1 = (a11*a11 + a12*a12 + a13*a13 + l2*l2 - l1*l1 - lb*lb) / (2*a13)
        r1 = p1*p1 + 4
        s1 = 2*p1*q1 + 4*lb
        t1 = q1*q1 + lb*lb - l2*l2

        p2 = (lb - a21) / a23
        q2 = (a21*a21 + a23*a23 - lb*lb + l2*l2 - l1*l1) / (2*a23)
        r2 = p2*p2 + 1
        s2 = 2*(p2*q2 - lb)
        t2 = q2*q2 - l2*l2 + lb*lb

        p3 = (-a31 - sqrt3*a32 - 2*lb) / a33
        q3 = (a31*a31 + a32*a32 + a33*a33 + l2*l2 - l1*l1 - lb*lb) / (2*a33)
        r3 = p3*p3 + 4
        s3 = 2*p3*q3 + 4*lb
        t3 = q3*q3 + lb*lb - l2*l2

        if not self.invert:
            c11 = (-s1 - math.sqrt(s1*s1 - 4*r1*t1)) / (2*r1)
            c12 = -sqrt3 * c11
            c13 = math.sqrt(l2*l2 - 4*(c11*c11) - 4*lb*c11 - lb*lb)
            self.C1 = [c11, c12, c13]

            c21 = (-s2 + math.sqrt(s2*s2 - 4*r2*t2)) / (2*r2)
            c22 = 0
            c23 = math.sqrt(l2*l2 - (c21 - lb)**2)
            self.C2 = [c21, c22, c23]

            c31 = (-s3 - math.sqrt(s3*s3 - 4*r3*t3)) / (2*r3)
            c32 = sqrt3 * c31
            c33 = math.sqrt(l2*l2 - 4*(c31*c31) - 4*lb*c31 - lb*lb)
            self.C3 = [c31, c32, c33]
        else:
            c11 = (-s1 - math.sqrt(s1*s1 - 4*r1*t1)) / (2*r1)
            c12 = -sqrt3 * c11
            c13 = math.sqrt(l2*l2 - 4*(c11*c11) - 4*lb*c11 - lb*lb)
            self.C1 = [c11, c12, -c13]

            c21 = (-s2 + math.sqrt(s2*s2 - 4*r2*t2)) / (2*r2)
            c22 = 0
            c23 = math.sqrt(l2*l2 - (c21 - lb)**2)
            self.C2 = [c21, c22, -c23]

            c31 = (-s3 - math.sqrt(s3*s3 - 4*r3*t3)) / (2*r3)
            c32 = sqrt3 * c31
            c33 = math.sqrt(l2*l2 - 4*(c31*c31) - 4*lb*c31 - lb*lb)
            self.C3 = [c31, c32, -c33]

    def solve_inverse_kinematics_vector(self, a, b, c, h):
        lb = self.lb
        self.B1 = [-0.5*lb, SQRT3*0.5*lb, 0]
        self.B2 = [lb, 0, 0]
        self.B3 = [-0.5*lb, -SQRT3*0.5*lb, 0]

        self.solve_top(a, b, c, h)
        self.solve_middle()

        self.theta1 = math.pi/2 - math.atan2(math.sqrt(self.C1[0]**2 + self.C1[1]**2) - lb, self.C1[2])
        self.theta2 = math.atan2(self.C2[2], self.C2[0] - lb)
        self.theta3 = math.pi/2 - math.atan2(math.sqrt(self.C3[0]**2 + self.C3[1]**2) - lb, self.C3[2])

    def solve_inverse_kinematics_spherical(self, theta, phi, h):
        self.h = h
        self.max_theta(h)
        theta = min(theta, self.maxtheta)

        a = math.sin(math.radians(theta)) * math.cos(math.radians(phi))
        b = math.sin(math.radians(theta)) * math.sin(math.radians(phi))
        c = math.cos(math.radians(theta))

        # Instead of try/except, validate inputs
        if not (math.isfinite(a) and math.isfinite(b) and math.isfinite(c)):
            return
        self.solve_inverse_kinematics_vector(a, b, c, h)

    def get_3d_coordinates_and_center(self):
        a1 = np.array(self.A1)
        a2 = np.array(self.A2)
        a3 = np.array(self.A3)
        center = (a1 + a2 + a3) / 3
        return {"A1": a1.tolist(), "A2": a2.tolist(), "A3": a3.tolist(), "center": center.tolist()}

    def max_theta(self, h, tol=1e-3):
        theta_low, theta_high = 0.0, math.radians(20)

        def valid(theta):
            c = math.cos(theta)
            for s in (1, -1):
                a21 = self.lp * c
                a23 = h - self.lp * (s * math.sin(theta))
                try:
                    p2 = (self.lb - a21) / a23
                    q2 = (a21*a21 + a23*a23 - self.lb*self.lb + self.l2*self.l2 - self.l1*self.l1) / (2 * a23)
                    r2 = p2*p2 + 1
                    s2 = 2 * (p2 * q2 - self.lb)
                    t2 = q2*q2 - self.l2*self.l2 + self.lb*self.lb
                    disc = s2*s2 - 4 * r2 * t2
                    if disc < 0: return False
                    c21 = (-s2 + math.sqrt(disc)) / (2 * r2)
                    delta = self.l2*self.l2 - (c21 - self.lb)**2
                    if delta < 0: return False
                    c23 = math.sqrt(delta)
                    if abs(math.sqrt((a21-c21)**2 + (a23-c23)**2) - self.l1) > 1e-3: return False
                    if abs(math.sqrt((self.lb-c21)**2 + c23**2) - self.l2) > 1e-3: return False
                except:
                    return False
            return True

        while theta_high - theta_low > tol:
            theta_mid = (theta_low + theta_high) / 2
            if valid(theta_mid):
                theta_low = theta_mid
            else:
                theta_high = theta_mid

        self.maxtheta = max(0, math.degrees(round(theta_low, 4)) - 0.5)
