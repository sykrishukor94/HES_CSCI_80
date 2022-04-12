from nim import *

# player = NimAI()
# game = Nim()
#
# # print(game.piles)
# # print(game.available_actions(game.piles))
#
# # # Test get_q_value
# # for action in game.available_actions(game.piles):
# #     print(player.get_q_value(tuple(game.piles), action))
#
# # Test best future reward
# print(player.best_future_reward(game.piles))



def test_get_q_value():

    # setup player
    player = NimAI()

    # setup dictionary
    player.q = {
            ((1, 2, 4, 4), (1, 2)): 1,
            ((1, 2, 4, 4), (1, 3)): None,
          }

    # Q value exist
    print(player.get_q_value([1, 2, 4, 4], (1, 2)))
    # no Q-value
    print(player.get_q_value([1, 2, 4, 4], (1, 3)))
    # no key
    print(player.get_q_value([1, 2, 4, 4], (1, 0)))

def test_best_future_reward():

    # setup player
    player = NimAI()

    # setup dictionary
    player.q = {
        # ((0, 1, 0, 2), (1, 1)): 0,
        ((0, 1, 0, 2), (1, 1)): None,
        ((0, 1, 0, 2), (3, 2)): -1,
        ((0, 1, 0, 2), (3, 1)): -0.99,
    }

    # test for
    print(player.best_future_reward([0, 1, 0, 2]))
    # test for no available actions in state
    print(player.best_future_reward([0, 0, 0, 0]))

def test_choose_action():
    # setup player
    player = NimAI()

    # setup dictionary
    player.q = {
        ((0, 1, 3, 2), (1, 1)): None,
        ((0, 1, 3, 2), (2, 1)): 0, # best action
        ((0, 1, 3, 2), (2, 2)): 0,
        ((0, 1, 3, 2), (2, 3)): -0.5,
        ((0, 1, 3, 2), (3, 1)): -0.5,
        ((0, 1, 3, 2), (3, 2)): -1, # best action
    }

    print(player.choose_action([0, 1, 3, 2], True))
    print(player.choose_action([0, 1, 3, 2], True))
    print(player.choose_action([0, 1, 3, 2], True))
    print(player.choose_action([0, 1, 3, 2], True))
    print(player.choose_action([0, 1, 3, 2], True))
    print(player.choose_action([0, 1, 3, 2], True))
    print(player.choose_action([0, 1, 3, 2], True))
    print(player.choose_action([0, 1, 3, 2], True))
    print(player.choose_action([0, 1, 3, 2], True))
    print(player.choose_action([0, 1, 3, 2], True))
    print(player.choose_action([0, 0, 0, 0], True))

def train(n):
    """
    Train an AI by playing `n` games against itself.
    """

    player = NimAI()

    # Play n games
    for i in range(n):
        print(f"Playing training game {i + 1}")
        game = Nim()

        # Keep track of last move made by either player
        last = {
            0: {"state": None, "action": None},
            1: {"state": None, "action": None}
        }

        # Game loop
        while True:

            # Keep track of current state and action
            state = game.piles.copy()
            action = player.choose_action(game.piles)

            # Keep track of last state and action
            last[game.player]["state"] = state
            last[game.player]["action"] = action

            # print(game.player, state, action)

            # Make move
            game.move(action)
            new_state = game.piles.copy()

            # When game is over, update Q values with rewards
            if game.winner is not None:
                player.update(state, action, new_state, -1)
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    1
                )
                break

            # If game is continuing, no rewards yet
            elif last[game.player]["state"] is not None:
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    0
                )
        # print(player.q)

    print("Done training")

    # Return the trained AI
    return player

def main():
    # test_get_q_value()
    # test_best_future_reward()
    # test_choose_action()
    ai = train(10000)
    list = sorted(ai.q.items(), key= lambda k : k[1], reverse=True)
    print(list)
    print(len(list))
    for i in range(5):
        play(ai)

if __name__ == "__main__":
    main()

