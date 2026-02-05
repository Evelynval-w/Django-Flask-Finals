/**
 * Dice Roller Module for NAHB
 * Handles dice rolling animations and logic
 */

class DiceRoller {
    constructor() {
        this.diceEmojis = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅'];
        this.rollDuration = 1000; // ms
        this.rollInterval = 100; // ms
    }
    
    /**
     * Simulate a dice roll with animation
     * @param {HTMLElement} displayElement - Element to show the dice
     * @param {number} finalValue - The predetermined result (1-6)
     * @returns {Promise} Resolves when animation completes
     */
    async animateRoll(displayElement, finalValue) {
        const iterations = this.rollDuration / this.rollInterval;
        
        for (let i = 0; i < iterations; i++) {
            const randomFace = Math.floor(Math.random() * 6);
            displayElement.textContent = this.diceEmojis[randomFace];
            await this.sleep(this.rollInterval);
        }
        
        // Show final result
        displayElement.textContent = this.diceEmojis[finalValue - 1];
        displayElement.classList.add('dice-landed');
        
        return finalValue;
    }
    
    /**
     * Check if a roll succeeds
     * @param {number} roll - The dice result
     * @param {number} required - Minimum required value
     * @returns {boolean}
     */
    checkSuccess(roll, required) {
        return roll >= required;
    }
    
    /**
     * Sleep helper
     * @param {number} ms - Milliseconds to sleep
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    /**
     * Generate a random dice roll (1-6)
     * @returns {number}
     */
    roll() {
        return Math.floor(Math.random() * 6) + 1;
    }
}

// Export for use
window.DiceRoller = DiceRoller;
