import numpy as np

# constants
GRID_DIM = (12, 12)     # columns x rows
PADDLE_HEIGHT = 0.2
(BALL_X_MIN, BALL_X_MAX) = (0*GRID_DIM[0], 1*GRID_DIM[0])
(BALL_Y_MIN, BALL_Y_MAX) = (0*GRID_DIM[1], 1*GRID_DIM[1])
DEFAULT_STATE = (0.5*GRID_DIM[0], 0.5*GRID_DIM[1], 0.03, 0.01, 0.5-PADDLE_HEIGHT/2)

# global variables
(ball_x, ball_y, velo_x, velo_y, paddle_y) = DEFAULT_STATE

def update_ball():
    '''Handles ball movements and logic for a single iteration in game loop. Returns reward value:
    -1  if update causes ball to passed agent's paddle (termination state);
    +1  if update results in a rebound by the paddle;
    0   otherwise (nothing significant happens).'''
    global ball_x, ball_y, velo_x, velo_y

    # ball positions are discretized into 2D grid slots, so velocity must be too when added
    ball_x += np.sign(velo_x)     #x velocity of 0 not allowed but won't occur b/c rebound check
    ball_y += np.sign(velo_y) if abs(velo_y) >= 0.015 else 0    #y unchanged if its velo < 0.015

    if ball_y < BALL_Y_MIN:
        # ball is below "screen" so flip pos & velo about y=0 line
        ball_y = -ball_y; velo_y = -velo_y
    elif ball_y > BALL_Y_MAX:
        # likewise, when above "screen", flip about y=MAX_Y line
        ball_y = 2*BALL_Y_MAX - ball_y; velo_y = -velo_y

    if ball_x < BALL_X_MIN:
        ball_x = -ball_x; velo_x = -velo_x
    elif ball_x >= BALL_X_MAX:
        if paddle_y == ball_y and ball_x == BALL_X_MAX:
            # notice this is after y pos is fully determined
            velo_y += np.random.uniform(-0.03, np.nextafter(0.03, 1))   #[-.03, +.03]
            velo_x = -velo_x + np.random.uniform(-0.015, np.nextafter(0.015, 1))
            if abs(velo_x) < 0.03:  #make sure that all |velocity_x| > 0.03
                velo_x = 0.03 if velo_x > 0 else -0.03
            return 1
        else:
            return -1   #ball is either passed paddle or not at the same y pos

    return 0    #nothing exciting happened

def main():
    pass

if __name__ == "__main__":
    main()
