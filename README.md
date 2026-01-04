# naruto-vs-sasuke
## Project OverviewThe game allows a player to control Naruto to fight against an automated Sasuke (enemy). It includes mechanics for movement, jumping, and projectile combat (shurikens) with a visual health bar system for both characters.

### Key Features
Sprite Animation: Uses image arrays to create smooth walking animations for both characters.
Projectile System: A weapons class handles the physics and life-cycle of shurikens thrown by the player.
Automated AI: Sasuke moves back and forth along a predefined path, acting as a dynamic target/opponent.
Collision Physics: Real-time hitbox calculation to detect when a shuriken hits the enemy or when characters collide.
Game States: Includes logic for health depletion, "Game Over" screens, and victory conditions for both sides.
SFX Integration: Integrated sound effects for hits and background music support.

## Technical Implementation
### Game Mechanics
Physics & Movement: * Naruto features a quadratic jump formula: $y = 0.5 \cdot \text{jumpheight}^2$.Directional tracking determines which way sprites face and projectiles travel.
Health Bars: * Dynamic health bars are rendered using pygame.draw.rect.Naruto’s bar fills left-to-right, while Sasuke’s bar is designed to deplete from right-to-left.
Class Structure:
player(): Manages user input, state, and drawing.
enemy(): Handles the automated patrol logic and health.
weapons(): Manages the velocity and hitboxes of shurikens.
## Controls
Left/Right Arrows: Move Naruto.
Up Arrow: Jump.
Spacebar: Throw Shuriken.
## Requirements
Python 3.x
Pygame Library: Install via pip install pygame.
Asset Folder: Requires a pics/ directory containing the specific .png sprites and .wav sound files referenced in the code.
