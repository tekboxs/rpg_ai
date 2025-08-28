"""
Dice System for RPG AI
Handles dice rolling and probability-based events
"""
from typing import Dict, List, Optional, Any, Tuple
import random
from ..utils.logger import logger

class DiceSystem:
    """Handles dice rolling and probability-based events"""
    
    def __init__(self):
        self.dice_history = []
        self.critical_success_threshold = 20  # Natural 20
        self.critical_failure_threshold = 1   # Natural 1
        
        logger.info("Dice System initialized")
    
    def roll_dice(self, dice_type: str = "d20", modifier: int = 0, advantage: bool = False, disadvantage: bool = False) -> Dict[str, Any]:
        """Roll dice with optional modifiers and advantage/disadvantage"""
        
        # Parse dice notation (e.g., "d20", "2d6", "d100")
        if dice_type.startswith('d'):
            dice_type = f"1{dice_type}"
        
        try:
            count, sides = map(int, dice_type.split('d'))
        except ValueError:
            logger.error(f"Invalid dice notation: {dice_type}")
            return self._create_roll_result(0, 0, dice_type, modifier, "Invalid dice notation")
        
        # Roll the dice
        if advantage and disadvantage:
            # Cancel each other out
            advantage = False
            disadvantage = False
        
        if advantage:
            roll1 = random.randint(1, sides)
            roll2 = random.randint(1, sides)
            roll_result = max(roll1, roll2)
            roll_details = f"Advantage: {roll1}, {roll2} (using {roll_result})"
        elif disadvantage:
            roll1 = random.randint(1, sides)
            roll2 = random.randint(1, sides)
            roll_result = min(roll1, roll2)
            roll_details = f"Disadvantage: {roll1}, {roll2} (using {roll_result})"
        else:
            roll_result = random.randint(1, sides)
            roll_details = str(roll_result)
        
        # Apply modifier
        final_result = roll_result + modifier
        
        # Determine if it's a critical success or failure
        critical_type = self._determine_critical(roll_result, sides)
        
        # Create result
        result = self._create_roll_result(roll_result, final_result, dice_type, modifier, roll_details, critical_type)
        
        # Store in history
        self.dice_history.append(result)
        
        logger.debug(f"Dice roll: {dice_type} + {modifier} = {final_result} ({roll_details})")
        return result
    
    def _create_roll_result(self, natural_roll: int, final_result: int, dice_type: str, modifier: int, roll_details: str, critical_type: str = None) -> Dict[str, Any]:
        """Create a standardized roll result"""
        return {
            'natural_roll': natural_roll,
            'final_result': final_result,
            'dice_type': dice_type,
            'modifier': modifier,
            'roll_details': roll_details,
            'critical_type': critical_type,
            'timestamp': self._get_timestamp()
        }
    
    def _determine_critical(self, roll: int, sides: int) -> Optional[str]:
        """Determine if a roll is a critical success or failure"""
        if sides == 20:  # Standard d20
            if roll == 20:
                return "critical_success"
            elif roll == 1:
                return "critical_failure"
        else:  # Other dice types
            if roll == sides:
                return "critical_success"
            elif roll == 1:
                return "critical_failure"
        return None
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def roll_ability_check(self, ability_score: int, difficulty_class: int, advantage: bool = False, disadvantage: bool = False) -> Dict[str, Any]:
        """Roll an ability check against a difficulty class"""
        
        # Calculate modifier from ability score
        modifier = (ability_score - 10) // 2
        
        # Roll d20
        roll_result = self.roll_dice("d20", modifier, advantage, disadvantage)
        
        # Determine success/failure
        success = roll_result['final_result'] >= difficulty_class
        margin = abs(roll_result['final_result'] - difficulty_class)
        
        # Add ability check specific info
        roll_result.update({
            'check_type': 'ability_check',
            'ability_score': ability_score,
            'difficulty_class': difficulty_class,
            'success': success,
            'margin': margin,
            'degree_of_success': self._determine_degree_of_success(roll_result['final_result'], difficulty_class, roll_result['critical_type'])
        })
        
        return roll_result
    
    def roll_attack(self, attack_bonus: int, armor_class: int, advantage: bool = False, disadvantage: bool = False) -> Dict[str, Any]:
        """Roll an attack roll against armor class"""
        
        # Roll d20
        roll_result = self.roll_dice("d20", attack_bonus, advantage, disadvantage)
        
        # Determine hit/miss
        hit = roll_result['final_result'] >= armor_class
        margin = abs(roll_result['final_result'] - armor_class)
        
        # Add attack specific info
        roll_result.update({
            'check_type': 'attack',
            'attack_bonus': attack_bonus,
            'armor_class': armor_class,
            'hit': hit,
            'margin': margin,
            'critical_hit': roll_result['critical_type'] == 'critical_success'
        })
        
        return roll_result
    
    def roll_damage(self, damage_dice: str, damage_bonus: int = 0) -> Dict[str, Any]:
        """Roll damage dice"""
        
        roll_result = self.roll_dice(damage_dice, damage_bonus)
        
        # Add damage specific info
        roll_result.update({
            'check_type': 'damage',
            'damage_dice': damage_dice,
            'damage_bonus': damage_bonus,
            'total_damage': roll_result['final_result']
        })
        
        return roll_result
    
    def roll_saving_throw(self, save_bonus: int, difficulty_class: int, advantage: bool = False, disadvantage: bool = False) -> Dict[str, Any]:
        """Roll a saving throw against a difficulty class"""
        
        # Roll d20
        roll_result = self.roll_dice("d20", save_bonus, advantage, disadvantage)
        
        # Determine save success/failure
        success = roll_result['final_result'] >= difficulty_class
        margin = abs(roll_result['final_result'] - difficulty_class)
        
        # Add saving throw specific info
        roll_result.update({
            'check_type': 'saving_throw',
            'save_bonus': save_bonus,
            'difficulty_class': difficulty_class,
            'success': success,
            'margin': margin,
            'degree_of_success': self._determine_degree_of_success(roll_result['final_result'], difficulty_class, roll_result['critical_type'])
        })
        
        return roll_result
    
    def _determine_degree_of_success(self, result: int, target: int, critical_type: str) -> str:
        """Determine the degree of success for a roll"""
        if critical_type == 'critical_success':
            return 'critical_success'
        elif critical_type == 'critical_failure':
            return 'critical_failure'
        elif result >= target + 10:
            return 'exceptional_success'
        elif result >= target + 5:
            return 'great_success'
        elif result >= target:
            return 'success'
        elif result >= target - 5:
            return 'near_success'
        else:
            return 'failure'
    
    def roll_random_event(self, event_type: str, difficulty: str = "medium") -> Dict[str, Any]:
        """Roll for a random event outcome"""
        
        difficulty_modifiers = {
            'very_easy': -5,
            'easy': -2,
            'medium': 0,
            'hard': 3,
            'very_hard': 6,
            'nearly_impossible': 10
        }
        
        modifier = difficulty_modifiers.get(difficulty, 0)
        
        # Roll d20
        roll_result = self.roll_dice("d20", modifier)
        
        # Determine event outcome
        outcome = self._determine_event_outcome(roll_result['final_result'], difficulty)
        
        # Add event specific info
        roll_result.update({
            'check_type': 'random_event',
            'event_type': event_type,
            'difficulty': difficulty,
            'outcome': outcome,
            'description': self._generate_event_description(event_type, outcome, roll_result)
        })
        
        return roll_result
    
    def _determine_event_outcome(self, result: int, difficulty: str) -> str:
        """Determine the outcome of a random event based on the roll result"""
        
        if result >= 25:
            return "legendary_success"
        elif result >= 20:
            return "amazing_success"
        elif result >= 15:
            return "great_success"
        elif result >= 10:
            return "success"
        elif result >= 5:
            return "partial_success"
        elif result >= 0:
            return "failure"
        elif result >= -5:
            return "bad_failure"
        else:
            return "catastrophic_failure"
    
    def _generate_event_description(self, event_type: str, outcome: str, roll_result: Dict) -> str:
        """Generate a description of the event outcome"""
        
        outcome_descriptions = {
            'legendary_success': 'acontece de forma extraordinária e memorável',
            'amazing_success': 'acontece de forma excepcional e impressionante',
            'great_success': 'acontece de forma muito boa',
            'success': 'acontece com sucesso',
            'partial_success': 'acontece parcialmente',
            'failure': 'falha em acontecer',
            'bad_failure': 'falha de forma problemática',
            'catastrophic_failure': 'falha de forma catastrófica'
        }
        
        description = outcome_descriptions.get(outcome, 'acontece de forma inesperada')
        
        if roll_result['critical_type'] == 'critical_success':
            description += ' (Sucesso Crítico!)'
        elif roll_result['critical_type'] == 'critical_failure':
            description += ' (Falha Crítica!)'
        
        return f"O evento {event_type} {description}."
    
    def get_dice_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent dice roll history"""
        return self.dice_history[-limit:] if self.dice_history else []
    
    def clear_dice_history(self) -> None:
        """Clear dice roll history"""
        self.dice_history.clear()
        logger.info("Dice history cleared")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get dice rolling statistics"""
        if not self.dice_history:
            return {'total_rolls': 0}
        
        total_rolls = len(self.dice_history)
        critical_successes = len([r for r in self.dice_history if r.get('critical_type') == 'critical_success'])
        critical_failures = len([r for r in self.dice_history if r.get('critical_type') == 'critical_failure'])
        
        return {
            'total_rolls': total_rolls,
            'critical_successes': critical_successes,
            'critical_failures': critical_failures,
            'critical_success_rate': critical_successes / total_rolls if total_rolls > 0 else 0,
            'critical_failure_rate': critical_failures / total_rolls if total_rolls > 0 else 0
        }
