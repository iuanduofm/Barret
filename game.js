// Game elements
const player = document.getElementById('player');
const obstacleContainer = document.getElementById('obstacle-container');
const powerupContainer = document.getElementById('powerup-container');
const gameMessage = document.getElementById('game-message');
const scoreElement = document.getElementById('score');
const highScoreElement = document.getElementById('highScore');
const jumpBtn = document.getElementById('jumpBtn');
const specialBtn = document.getElementById('specialBtn');
const restartBtn = document.getElementById('restartBtn');

// Game state
const game = {
    isRunning: false,
    speed: 5,
    score: 0,
    highScore: parseInt(localStorage.getItem('dinoHighScore') || 0),
    obstacleTimer: null,
    powerupTimer: null,
    animationFrame: null,
    obstacles: [],
    powerups: [],
    specialPowerActive: false,
    specialCooldown: false,
    difficultyLevel: 1
};

// Update high score display
highScoreElement.textContent = game.highScore;

// Sound effects (empty Audio objects that could be replaced with real sounds)
const sounds = {
    jump: new Audio(),
    die: new Audio(),
    powerup: new Audio(),
    special: new Audio()
};

// Game functions
function startGame() {
    if (!game.isRunning) {
        resetGame();
        game.isRunning = true;
        gameMessage.style.display = 'none';
        
        // Start spawning obstacles and powerups
        game.obstacleTimer = setInterval(spawnObstacle, 2000);
        game.powerupTimer = setInterval(spawnPowerup, 7000);
        
        // Start game loop
        gameLoop();
    }
}

function resetGame() {
    // Clear existing obstacles and powerups
    obstacleContainer.innerHTML = '';
    powerupContainer.innerHTML = '';
    game.obstacles = [];
    game.powerups = [];
    
    // Reset game state
    game.score = 0;
    game.speed = 5;
    game.difficultyLevel = 1;
    game.specialPowerActive = false;
    game.specialCooldown = false;
    specialBtn.disabled = false;
    
    // Reset score display
    scoreElement.textContent = game.score;
    
    // Clear timers
    if (game.obstacleTimer) clearInterval(game.obstacleTimer);
    if (game.powerupTimer) clearInterval(game.powerupTimer);
    if (game.animationFrame) cancelAnimationFrame(game.animationFrame);
}

function gameOver() {
    game.isRunning = false;
    gameMessage.style.display = 'block';
    gameMessage.textContent = 'Game Over! Click to Restart';
    gameMessage.style.color = '#ff5252';
    
    // Play sound
    playSoundEffect('die');
    
    // Update high score
    if (game.score > game.highScore) {
        game.highScore = game.score;
        localStorage.setItem('dinoHighScore', game.highScore);
        highScoreElement.textContent = game.highScore;
        gameMessage.textContent = 'New High Score! Click to Restart';
        gameMessage.style.color = '#ffeb3b';
    }
    
    // Clear timers
    if (game.obstacleTimer) clearInterval(game.obstacleTimer);
    if (game.powerupTimer) clearInterval(game.powerupTimer);
    if (game.animationFrame) cancelAnimationFrame(game.animationFrame);
}

function updateScore() {
    game.score++;
    scoreElement.textContent = game.score;
    
    // Increase difficulty every 100 points
    if (game.score % 100 === 0) {
        increaseDifficulty();
    }
}

function increaseDifficulty() {
    game.difficultyLevel++;
    game.speed += 0.5;
    
    // Decrease obstacle spawn interval
    clearInterval(game.obstacleTimer);
    const newInterval = Math.max(800, 2000 - (game.difficultyLevel * 100));
    game.obstacleTimer = setInterval(spawnObstacle, newInterval);
    
    // Visual feedback for level up
    gameMessage.textContent = 'Level Up!';
    gameMessage.style.display = 'block';
    gameMessage.style.color = '#ffeb3b';
    
    setTimeout(() => {
        if (game.isRunning) {
            gameMessage.style.display = 'none';
        }
    }, 1000);
    
    playSoundEffect('powerup');
}

function playSoundEffect(soundName) {
    // Uncomment to enable sound effects when you have actual audio files
    // sounds[soundName].currentTime = 0;
    // sounds[soundName].play().catch(() => {});
}

// Player actions
function jump() {
    if (game.isRunning && !player.classList.contains('jumping')) {
        player.classList.add('jumping');
        playSoundEffect('jump');
        
        setTimeout(() => {
            player.classList.remove('jumping');
        }, 600); // Match with CSS animation duration
    }
}

function useSpecialPower() {
    if (game.isRunning && !game.specialCooldown) {
        // Activate fire breath
        game.specialPowerActive = true;
        player.classList.add('fire-breath');
        specialBtn.disabled = true;
        playSoundEffect('special');
        
        // Burn all obstacles in path
        burnObstacles();
        
        // Deactivate after a short time
        setTimeout(() => {
            game.specialPowerActive = false;
            player.classList.remove('fire-breath');
        }, 1000);
        
        // Cooldown period
        game.specialCooldown = true;
        setTimeout(() => {
            game.specialCooldown = false;
            specialBtn.disabled = false;
        }, 10000); // 10-second cooldown
    }
}

function burnObstacles() {
    game.obstacles.forEach(obstacle => {
        const obstacleEl = document.getElementById(obstacle.id);
        if (obstacleEl && obstacle.x > 50 && obstacle.x < 300) {
            // Visual effect for burning
            obstacleEl.style.transform = 'scale(0.1)';
            obstacleEl.style.opacity = '0';
            obstacleEl.style.transition = 'all 0.5s';
            
            // Remove after animation
            setTimeout(() => {
                if (obstacleEl.parentNode) {
                    obstacleEl.parentNode.removeChild(obstacleEl);
                }
            }, 500);
            
            // Award bonus points
            game.score += 5;
            scoreElement.textContent = game.score;
        }
    });
    
    // Filter out burned obstacles
    game.obstacles = game.obstacles.filter(obstacle => {
        const obstacleEl = document.getElementById(obstacle.id);
        return obstacleEl && obstacleEl.style.opacity !== '0';
    });
}

// Game elements spawning
function spawnObstacle() {
    if (!game.isRunning) return;
    
    const obstacleId = 'obstacle-' + Date.now();
    const obstacle = {
        id: obstacleId,
        x: window.innerWidth,
        type: Math.floor(Math.random() * 3) // 0-2: different obstacles
    };
    
    // Create obstacle element
    const obstacleEl = document.createElement('div');
    obstacleEl.className = 'obstacle';
    obstacleEl.id = obstacleId;
    obstacleEl.style.left = obstacle.x + 'px';
    
    // Different types of obstacles
    if (obstacle.type === 0) {
        // Small obstacle
        obstacleEl.style.height = '40px';
        obstacleEl.style.width = '30px';
    } else if (obstacle.type === 1) {
        // Tall obstacle
        obstacleEl.style.height = '70px';
        obstacleEl.style.width = '40px';
    } else {
        // Wide obstacle
        obstacleEl.style.height = '50px';
        obstacleEl.style.width = '60px';
    }
    
    obstacleContainer.appendChild(obstacleEl);
    game.obstacles.push(obstacle);
}

function spawnPowerup() {
    if (!game.isRunning) return;
    
    const powerupId = 'powerup-' + Date.now();
    const powerup = {
        id: powerupId,
        x: window.innerWidth,
        y: 100 + Math.random() * 150, // Random height
        type: Math.floor(Math.random() * 2) // 0-1: different powerups
    };
    
    // Create powerup element
    const powerupEl = document.createElement('div');
    powerupEl.className = 'powerup';
    powerupEl.id = powerupId;
    powerupEl.style.left = powerup.x + 'px';
    powerupEl.style.bottom = powerup.y + 'px';
    
    powerupContainer.appendChild(powerupEl);
    game.powerups.push(powerup);
}

// Collision detection
function checkCollisions() {
    const playerRect = player.getBoundingClientRect();
    
    // Check obstacle collisions
    game.obstacles.forEach((obstacle, index) => {
        const obstacleEl = document.getElementById(obstacle.id);
        if (obstacleEl) {
            const obstacleRect = obstacleEl.getBoundingClientRect();
            
            // Check if collision occurs
            if (
                playerRect.right > obstacleRect.left + 15 &&
                playerRect.left < obstacleRect.right - 15 &&
                playerRect.bottom > obstacleRect.top + 10 &&
                playerRect.top < obstacleRect.bottom - 10 &&
                !game.specialPowerActive // No collision during special power
            ) {
                gameOver();
            }
            
            // Remove off-screen obstacles
            if (obstacle.x < -100) {
                obstacleEl.remove();
                game.obstacles.splice(index, 1);
                updateScore();
            }
        }
    });
    
    // Check powerup collisions
    game.powerups.forEach((powerup, index) => {
        const powerupEl = document.getElementById(powerup.id);
        if (powerupEl) {
            const powerupRect = powerupEl.getBoundingClientRect();
            
            // Check if player collects powerup
            if (
                playerRect.right > powerupRect.left &&
                playerRect.left < powerupRect.right &&
                playerRect.bottom > powerupRect.top &&
                playerRect.top < powerupRect.bottom
            ) {
                collectPowerup(powerup, index);
                powerupEl.remove();
                game.powerups.splice(index, 1);
            }
            
            // Remove off-screen powerups
            if (powerup.x < -50) {
                powerupEl.remove();
                game.powerups.splice(index, 1);
            }
        }
    });
}

function collectPowerup(powerup, index) {
    playSoundEffect('powerup');
    
    // Different powerup effects
    if (powerup.type === 0) {
        // Score boost
        game.score += 20;
        scoreElement.textContent = game.score;
        
        // Visual feedback
        showFloatingText('+20', player.offsetLeft, player.offsetTop - 20);
    } else {
        // Special power recharge
        game.specialCooldown = false;
        specialBtn.disabled = false;
        
        // Visual feedback
        showFloatingText('Special Ready!', player.offsetLeft, player.offsetTop - 20);
    }
}

function showFloatingText(text, x, y) {
    const floatingText = document.createElement('div');
    floatingText.innerText = text;
    floatingText.style.position = 'absolute';
    floatingText.style.left = x + 'px';
    floatingText.style.top = y + 'px';
    floatingText.style.color = '#ffeb3b';
    floatingText.style.fontWeight = 'bold';
    floatingText.style.zIndex = '100';
    floatingText.style.pointerEvents = 'none';
    document.body.appendChild(floatingText);
    
    // Animate floating up and fading out
    let opacity = 1;
    let posY = y;
    
    const animateText = () => {
        opacity -= 0.02;
        posY -= 1;
        floatingText.style.opacity = opacity;
        floatingText.style.top = posY + 'px';
        
        if (opacity > 0) {
            requestAnimationFrame(animateText);
        } else {
            floatingText.remove();
        }
    };
    
    requestAnimationFrame(animateText);
}

// Game loop
function gameLoop() {
    if (!game.isRunning) return;
    
    // Update obstacle positions
    game.obstacles.forEach(obstacle => {
        obstacle.x -= game.speed;
        const obstacleEl = document.getElementById(obstacle.id);
        if (obstacleEl) {
            obstacleEl.style.left = obstacle.x + 'px';
        }
    });
    
    // Update powerup positions
    game.powerups.forEach(powerup => {
        powerup.x -= game.speed;
        const powerupEl = document.getElementById(powerup.id);
        if (powerupEl) {
            powerupEl.style.left = powerup.x + 'px';
        }
    });
    
    // Check for collisions
    checkCollisions();
    
    // Continue game loop
    game.animationFrame = requestAnimationFrame(gameLoop);
}

// Event listeners
document.addEventListener('keydown', (e) => {
    if (e.code === 'Space') {
        if (!game.isRunning) {
            startGame();
        } else {
            jump();
        }
        e.preventDefault();
    } else if (e.code === 'KeyS' || e.code === 'ArrowDown') {
        useSpecialPower();
        e.preventDefault();
    }
});

document.getElementById('game-canvas-container').addEventListener('click', () => {
    if (!game.isRunning) {
        startGame();
    }
});

jumpBtn.addEventListener('click', () => {
    if (!game.isRunning) {
        startGame();
    } else {
        jump();
    }
});

specialBtn.addEventListener('click', useSpecialPower);

restartBtn.addEventListener('click', () => {
    resetGame();
    startGame();
});

// Mobile touch support
document.addEventListener('touchstart', (e) => {
    if (!game.isRunning) {
        startGame();
        e.preventDefault();
    }
});

// Initialize game message
gameMessage.addEventListener('click', () => {
    if (!game.isRunning) {
        startGame();
    }
}); 