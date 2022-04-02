from nim import train, play

ai = train(10000)
for i in range(10):
    play(ai)
