"""Student Grade Calculator

This program manages student records, accepts test scores, calculates
an average score, and determines a letter grade.
"""

import os
from typing import Dict, List


def get_string_input(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be blank. Please try again.")


def get_float_input(prompt: str, min_value: float = 0.0, max_value: float = 100.0) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value < min_value or value > max_value:
                raise ValueError
            return value
        except ValueError:
            print(f"Please enter a valid number between {min_value} and {max_value}.")


def calculate_average(scores: List[float]) -> float:
    return sum(scores) / len(scores)


def determine_letter_grade(average: float) -> str:
    if average >= 90:
        return "A"
    if average >= 80:
        return "B"
    if average >= 70:
        return "C"
    if average >= 60:
        return "D"
    return "F"


def create_student_record() -> Dict[str, object]:
    print("\nEnter student record")
    name = get_string_input("Student name: ")
    student_id = get_string_input("Student ID: ")
    test1 = get_float_input("Test 1 score: ")
    test2 = get_float_input("Test 2 score: ")
    test3 = get_float_input("Test 3 score: ")

    average = calculate_average([test1, test2, test3])
    letter = determine_letter_grade(average)

    return {
        "name": name,
        "id": student_id,
        "test1": test1,
        "test2": test2,
        "test3": test3,
        "average": average,
        "grade": letter,
    }


def display_student_record(record: Dict[str, object]) -> None:
    print("\nStudent Record")
    print("--------------")
    print(f"Name: {record['name']}")
    print(f"Student ID: {record['id']}")
    print(f"Test 1: {record['test1']:.2f}")
    print(f"Test 2: {record['test2']:.2f}")
    print(f"Test 3: {record['test3']:.2f}")
    print(f"Average Score: {record['average']:.2f}")
    print(f"Letter Grade: {record['grade']}")


def display_all_records(records: List[Dict[str, object]]) -> None:
    if not records:
        print("\nNo student records available.")
        return

    print("\nStudent Records - Table View")
    print("=" * 85)
    print(f"{'Name':<20} {'Student ID':<12} {'Test 1':<10} {'Test 2':<10} {'Test 3':<10} {'Average':<10} {'Grade':<5}")
    print("-" * 85)
    
    for record in records:
        print(f"{str(record['name']):<20} {str(record['id']):<12} {record['test1']:<10.2f} {record['test2']:<10.2f} {record['test3']:<10.2f} {record['average']:<10.2f} {str(record['grade']):<5}")
    
    print("=" * 85)


def calculate_class_statistics(records: List[Dict[str, object]]) -> Dict[str, float]:
    """Calculate highest, lowest, and class average."""
    if not records:
        return {}
    
    averages = [record["average"] for record in records]
    return {
        "highest": max(averages),
        "lowest": min(averages),
        "class_average": sum(averages) / len(averages)
    }


def display_class_statistics(records: List[Dict[str, object]]) -> None:
    """Display class statistics."""
    if not records:
        print("\nNo student records available for statistics.")
        return
    
    stats = calculate_class_statistics(records)
    print("\nClass Statistics")
    print("=" * 40)
    print(f"Highest Average: {stats['highest']:.2f}")
    print(f"Lowest Average: {stats['lowest']:.2f}")
    print(f"Class Average: {stats['class_average']:.2f}")
    print(f"Total Students: {len(records)}")
    print("=" * 40)


def search_student(records: List[Dict[str, object]], name: str) -> List[Dict[str, object]]:
    """Search for students by name (case-insensitive)."""
    search_name = name.lower().strip()
    results = [record for record in records if search_name in record["name"].lower()]
    return results


def display_search_results(results: List[Dict[str, object]], search_name: str) -> None:
    """Display search results."""
    if not results:
        print(f"\nNo students found with name containing '{search_name}'.")
        return
    
    print(f"\nSearch Results for '{search_name}'")
    print("=" * 85)
    print(f"{'Name':<20} {'Student ID':<12} {'Test 1':<10} {'Test 2':<10} {'Test 3':<10} {'Average':<10} {'Grade':<5}")
    print("-" * 85)
    
    for record in results:
        print(f"{str(record['name']):<20} {str(record['id']):<12} {record['test1']:<10.2f} {record['test2']:<10.2f} {record['test3']:<10.2f} {record['average']:<10.2f} {str(record['grade']):<5}")
    
    print("=" * 85)


def save_records(records: List[Dict[str, object]], filename: str = "student_grades.txt") -> None:
    """Save student records to a pipe-delimited file."""
    try:
        with open(filename, "w") as file:
            # Write header
            file.write("name|id|test1|test2|test3|average|grade\n")
            # Write records
            for record in records:
                line = f"{record['name']}|{record['id']}|{record['test1']:.2f}|{record['test2']:.2f}|{record['test3']:.2f}|{record['average']:.2f}|{record['grade']}\n"
                file.write(line)
        print(f"Records saved to {filename}")
    except IOError as e:
        print(f"Error saving records: {e}")


def load_records(filename: str = "student_grades.txt") -> List[Dict[str, object]]:
    """Load student records from a pipe-delimited file."""
    if not os.path.exists(filename):
        return []
    
    records = []
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
            
        if not lines:
            return []
        
        # Skip header line
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            
            try:
                parts = line.split("|")
                if len(parts) != 7:
                    print(f"Warning: Skipping invalid line: {line}")
                    continue
                
                record = {
                    "name": parts[0],
                    "id": parts[1],
                    "test1": float(parts[2]),
                    "test2": float(parts[3]),
                    "test3": float(parts[4]),
                    "average": float(parts[5]),
                    "grade": parts[6],
                }
                records.append(record)
            except (ValueError, IndexError) as e:
                print(f"Warning: Error parsing line '{line}': {e}")
                continue
        
        if records:
            print(f"Loaded {len(records)} student record(s) from {filename}")
        return records
    except IOError as e:
        print(f"Error loading records: {e}")
        return []



def main() -> None:
    records: List[Dict[str, object]] = load_records()

    while True:
        try:
            print("\n" + "=" * 50)
            print("Student Grade Calculator")
            print("=" * 50)
            print("1. Add a student record")
            print("2. View all student records")
            print("3. View class statistics")
            print("4. Search for a student")
            print("5. Exit")
            print("=" * 50)

            choice = input("Choose an option (1-5): ").strip()
            
            if choice == "1":
                record = create_student_record()
                records.append(record)
                print("Student record saved.")
                save_records(records)
            elif choice == "2":
                display_all_records(records)
            elif choice == "3":
                display_class_statistics(records)
            elif choice == "4":
                search_name = get_string_input("Enter student name to search: ")
                results = search_student(records, search_name)
                display_search_results(results, search_name)
            elif choice == "5":
                print("\nExiting the Student Grade Calculator. Goodbye!")
                break
            else:
                print("Invalid selection. Please enter 1, 2, 3, 4, or 5.")
        except KeyboardInterrupt:
            print("\n\nExiting the Student Grade Calculator. Goodbye!")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
