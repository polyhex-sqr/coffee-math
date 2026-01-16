#!/usr/bin/env python3
"""
Filter Coffee Calculator

Calculate water, milk, and coffee amounts for filter coffee based on:
- Cup sizes (ml)
- Milk-to-coffee ratios
- Beans per 100ml ratio

This script provides a readable version of the calculations performed in index.html
"""

import argparse
from typing import List, Tuple


def calculate_coffee_amounts(
    cup_sizes: List[float],
    milk_ratios: List[float],
    beans_per_100ml: float = 6.0
) -> Tuple[float, float, float]:
    """
    Calculate water, milk, and coffee amounts for filter coffee.

    Args:
        cup_sizes: List of cup sizes in milliliters
        milk_ratios: List of milk-to-coffee ratios (0-1) for each cup
        beans_per_100ml: Grams of coffee beans per 100ml of coffee (default: 6.0)

    Returns:
        Tuple of (water_ml, milk_ml, coffee_g)

    Formula:
        - coffee_sizes = sum(cup_size * (1 - milk_ratio))
        - water_ml = coffee_sizes / 0.9  (accounts for coffee absorption)
        - milk_ml = sum(cup_size * milk_ratio)
        - coffee_g = coffee_sizes / 100 * beans_per_100ml
    """
    if len(cup_sizes) != len(milk_ratios):
        raise ValueError("cup_sizes and milk_ratios must have the same length")

    # Clamp milk ratios to valid range [0, 1] and calculate totals
    coffee_sizes = 0.0
    milk_ml = 0.0

    for cup_size, milk_ratio in zip(cup_sizes, milk_ratios):
        # Clamp milk ratio to valid range [0, 1]
        clamped_ratio = max(0.0, min(1.0, milk_ratio))
        
        # Calculate coffee volume for this cup (excluding milk)
        coffee_sizes += cup_size * (1 - clamped_ratio)
        
        # Calculate milk volume for this cup
        milk_ml += cup_size * clamped_ratio

    # Calculate water needed (accounting for ~10% absorption by coffee grounds)
    water_ml = coffee_sizes / 0.9

    # Calculate coffee beans weight
    coffee_g = coffee_sizes / 100 * beans_per_100ml

    return water_ml, milk_ml, coffee_g


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Calculate water, milk, and coffee amounts for filter coffee",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --cup-sizes 300 --milk-ratios 0.25
  %(prog)s --cup-sizes 300,240 --milk-ratios 0.25,0.3 --beans-per-100ml 6.5
        """
    )
    
    parser.add_argument(
        "--cup-sizes",
        type=str,
        default="300",
        help="Comma-separated list of cup sizes in milliliters (default: 300)"
    )
    
    parser.add_argument(
        "--milk-ratios",
        type=str,
        default="0.25",
        help="Comma-separated list of milk-to-coffee ratios (0-1) for each cup (default: 0.25)"
    )
    
    parser.add_argument(
        "--beans-per-100ml",
        type=float,
        default=6.0,
        help="Grams of coffee beans per 100ml of coffee (default: 6.0)"
    )
    
    return parser.parse_args()


def main():
    """Main function with command-line argument parsing."""
    args = parse_args()
    
    # Parse comma-separated values
    try:
        cup_sizes = [float(x.strip()) for x in args.cup_sizes.split(",")]
        milk_ratios = [float(x.strip()) for x in args.milk_ratios.split(",")]
    except ValueError as e:
        print(f"Error: Invalid input format. Please use comma-separated numbers.\n{e}")
        return
    
    beans_per_100ml = args.beans_per_100ml
    
    # Validate inputs
    if len(cup_sizes) != len(milk_ratios):
        print(f"Error: Number of cup sizes ({len(cup_sizes)}) must match number of milk ratios ({len(milk_ratios)})")
        return
    
    if any(size <= 0 for size in cup_sizes):
        print("Error: All cup sizes must be greater than 0")
        return
    
    if beans_per_100ml <= 0:
        print("Error: Beans per 100ml must be greater than 0")
        return

    # Calculate amounts
    water_ml, milk_ml, coffee_g = calculate_coffee_amounts(
        cup_sizes, milk_ratios, beans_per_100ml
    )

    # Print results
    print("Filter Coffee Calculator Results")
    print("=" * 40)
    print(f"Water (ml):     {water_ml:.1f}")
    print(f"Milk (ml):      {milk_ml:.1f}")
    print(f"Coffee (g):      {coffee_g:.1f}")
    print("=" * 40)
    print()
    print(f"Cup sizes:      {cup_sizes} ml")
    print(f"Milk ratios:    {milk_ratios}")
    print(f"Beans/100ml:    {beans_per_100ml} g")


if __name__ == "__main__":
    main()
