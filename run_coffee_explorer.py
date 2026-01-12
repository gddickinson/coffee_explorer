#!/usr/bin/env python3
"""
Coffee Collection Explorer - Application Launcher
Run this script to start the Coffee Collection Explorer GUI application
"""

import sys
import os

# Ensure we're in the right directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Run the coffee explorer
import coffee_explorer

if __name__ == "__main__":
    print("="*60)
    print("  COFFEE COLLECTION EXPLORER")
    print("="*60)
    print("\nStarting the Coffee Collection Explorer...")
    print("Features:")
    print("  • Browse 29 coffee origins worldwide")
    print("  • Explore 20 coffee varieties/cultivars")
    print("  • Discover 28 coffee roasters & brands")
    print("  • Learn 12 brewing methods")
    print("  • Keep a tasting journal")
    print("  • Interactive world map of coffee regions")
    print("\nLoading application...")
    print("="*60)
    print()
    
    coffee_explorer.main()
