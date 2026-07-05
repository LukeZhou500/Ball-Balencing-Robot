
import math



class PIDController:

    def __init__(self, kp=1.0, ki=0.0, kd=0.0, kv=0.0,

                 integral_limit=10.0,

                 derivative_filter=0.2,   # 0–1 smoothing

                 velocity_cutoff=5.0,    # cutoff freq [Hz]

                 dt_guess=0.01):

        self.kp = kp

        self.ki = ki

        self.kd = kd

        self.kv = kv



        self.integral_limit = integral_limit

        self.derivative_filter = derivative_filter

        self.velocity_cutoff = velocity_cutoff



        self.prev_error = 0.0

        self.prev_time = None

        self.integral = 0.0



        # filtered derivative and velocity

        self.d_error_filtered = 0.0

        self.vel_filtered = 0.0



        self.dt_guess = dt_guess



    def update(self, error, current_time):

        # compute dt

        if self.prev_time is None:

            dt = self.dt_guess

        else:

            dt = max(current_time - self.prev_time, 0.0005)



        # proportional

        p_term = self.kp * error



        # integral (with windup guard)

        self.integral += error * dt

        self.integral = max(-self.integral_limit, min(self.integral, self.integral_limit))

        i_term = self.ki * self.integral



        # derivative (on error)

        d_error = (error - self.prev_error) / dt

        # simple low-pass filter for derivative

        alpha_d = self.derivative_filter

        self.d_error_filtered = (1 - alpha_d) * self.d_error_filtered + alpha_d * d_error

        d_term = self.kd * self.d_error_filtered



        # velocity damping (opposite to error speed)

        # use same filtered derivative as velocity estimate, but with its own cutoff

        rc = 1.0 / (2 * math.pi * self.velocity_cutoff)

        alpha_v = dt / (rc + dt)

        self.vel_filtered = (1 - alpha_v) * self.vel_filtered + alpha_v * d_error

        v_term = self.kv * self.vel_filtered * abs(pow(d_error,0.65))/7



        # save state

        self.prev_error = error

        self.prev_time = current_time


        pidv = p_term + i_term + d_term + v_term
        if abs(pidv) > 40:
            return 40
        else:
            return pidv
