import logging
import random


class SweepstakeGenerator:
    def __init__(self) -> None:
        self.setup_logger()
        self.people_list = "people_list.txt"
        self.item_list = "items_list.txt"

    def setup_logger(self) -> None:
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
        )

    def assign(self, people, items):
        print(f"items 2: {items}({len(items)})")
        print(f"people 2: {people}")

        random.shuffle(items)

        assignments = {}

        items_per_person_rounded_up = round(len(items) / len(people))

        for i in range(items_per_person_rounded_up):
            if not len(items) < len(people):
                for person in people:
                    assigned_item = items.pop()
                    assignments[person] = assigned_item
        
                print(f"items post assignment round {i}: {items}({len(items)})")
            else:
                # TO DO: How do i deal with more people then items?
                reply = len(items) / len(people)

        return assignments


def main():
    items = ['Avi Sharma', 'Bradley Johnson', 'Dani Donovan', 'Denisha Kaur Bharj', 'Emma Browne', 'Gregory Ebbs', 'Joe Phillips', 'Kevin D\'Arcy', 'Mark Moseley', 'Marnie Swindells', 'Megan Hornby', 'Reece Donnelly', 'Rochelle Anthony', 'Shannon Martin', 'Shazia Hussain', 'Simba Rwambiwa', 'Sohail Chowdhary', 'Victoria Goulbourne']
    people = ['Tim', 'Jake', 'Katie', 'Paul']
    sweepstake_generator = SweepstakeGenerator()
    print(f"items: {items}")
    print(f"people: {people}")
    result = sweepstake_generator.assign(people, items)
    
    for person, assigned_items in result.items():
        print(f"{person}: {', '.join(assigned_items)}")


if __name__ == "__main__":
    main()
