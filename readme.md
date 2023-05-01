# Title: Sssserpent Struggle: A Reinvented Classic Snake Game

### Inspiration 🌟
Nostalgia often brings back cherished memories and takes us on a journey down memory lane. To pay homage to the classic games that have entertained generations, we present our own take on the iconic Snake Game. By leveraging Python and the Pygame library, we aim to revive the magic of this retro game while showcasing its potential for a new generation of players.

### Game Overview and Rules
Introducing Sssserpent Struggle, a reimagined version of the classic snake game that adds a new twist to the original gameplay!

The game is designed to test your skills and strategy as you navigate your snake through the playing field, consuming pellets to grow in length, just like the original game. However, in this iteration, you must also be wary of enemy snakes that are pursuing the same food using **greedy path-finding algorithm**.

Collisions with other snakes can have deadly consequences. If one snake collides with the body of another snake, the snake loses length from where it got hit, making it harder to survive. But if two snakes collide head-first, it's game over for the shorter snake, and if it's your snake that's hit, you'll have to start over.

Our game has been designed with both nostalgia and innovation in mind. The gameplay is inspired by the original snake game that we all know and love, but with the added challenge of facing off against other intelligent snakes.

### Key Features ⚡
- Simplistic yet visually appealing design
- Smooth and responsive gameplay mechanics
- Gradually increasing difficulty as the snake grows in length
- Four enemy snakes with advanced path-finding algorithms that compete for pellets with the player's snake
- Blocks that obstruct the player's snake and require strategic navigation to avoid or overcome

### How We Built It 🔧
We built **Sssserpent Struggle** using the Pygame library, which provided us with the necessary tools to create a smooth and responsive game. We implemented a game loop and various game components, including the snake, food, blocks and game boundaries. The snake's movements and the food's spawning locations were carefully designed to create a challenging yet enjoyable experience for the player. We also had to build a **greedy path-finding algorithm** for the enemy snakes, which proved to be one of the most challenging aspects of development.

After a set time interval, **four enemy snakes** are added to the playing field, each with its own path-finding algorithm, increasing the level of difficulty for the player.

### Installation and Gameplay Instructions

> #### Windows Users
> 1. To download and play the game, you can find it conveniently published on itch.io. Simply visit the following link: https://rajsudharshan.itch.io/sssserpent-struggle.
> 2. Download the game executable file (snake.exe) and the image file (blocks.png) from the website.
> 3. Save both files in the same folder or directory on your computer.
> 4. Open the folder or directory where you saved the files.
> 5. Double-click on the snake.exe file to run the game. 
> 6. If you see a warning message stating that Windows has protected your PC, click on "More info".
> 7. Click on "Run anyway" to run the game.
> 8. The game should start and you should be able to play it. 

> #### Mac Users
> 1. Open the terminal on your Mac.
> 2. Clone the GitHub repository by executing the command:
 `git clone https://github.com/RAJ-SUDHARSHAN/Sssserpent-Struggle.git`
> 3. Navigate to the cloned repository's directory.
> 4. Install the required dependencies by running the command: 
`pip install -r requirements.txt`
> 5. Start playing the game by entering the command: 
`python snake.py`

### Challenges We Faced 🚧
One of the main challenges we faced during development was building the greedy path-finding algorithm for the enemy snakes. This algorithm needed to be **efficient and intelligent** enough to allow the enemy snakes to effectively compete for the pellets with the player's snake. We spent many hours researching and testing different algorithms to find the best solution for our game.

In addition to this, we also faced challenges in ensuring smooth and responsive gameplay, designing a visually appealing interface true to the original game, and maintaining code efficiency and optimization for seamless performance. Despite these difficulties, we were able to overcome them and create an engaging and enjoyable game that we are proud of.

### Accomplishments We're Proud Of 🏆
- Successfully recreating and enhancing the Classic Snake Game using Python and Pygame
- Overcoming challenges in optimizing code and maintaining smooth gameplay
- Providing a nostalgic and engaging gaming experience for players of all ages

### What We Learned 📚
- Deeper understanding of Python and the Pygame library
- Implementing efficient solutions for game components and mechanics
- Importance of code optimization and performance tuning

### What's Next for the Enhanced Classic Snake Game 🚀
We envision expanding upon our Enhanced Classic Snake Game to offer an even more immersive experience for players. Potential future updates include:

- Implementing new game modes and challenges
- Adding multiplayer functionality for an engaging social experience
- Incorporating a global leaderboard system to encourage competition among players
- Offering customizable snake and background designs for personalization
