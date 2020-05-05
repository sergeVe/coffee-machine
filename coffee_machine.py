class CoffeeMachine:
    @staticmethod
    def _espresso_unit_subtract():
        espresso_water_quantity = 250
        espresso_beans_quantity = 16
        espresso_cup_cost = 4
        return [espresso_cup_cost, -espresso_water_quantity, 0, -espresso_beans_quantity, -1]

    @staticmethod
    def _latte_unit_subtract():
        # latte constants
        latte_water_quantity = 350
        latte_milk_quantity = 75
        latte_beans_quantity = 20
        latte_cup_cost = 7
        return [latte_cup_cost, -latte_water_quantity, -latte_milk_quantity, -latte_beans_quantity, -1]

    @staticmethod
    def _cappucino_unit_subtract():
        # cappuccino constants
        cappuccino_water_quantity = 200
        cappuccino_milk_quantity = 100
        cappuccino_beans_quantity = 12
        cappuccino_cup_cost = 6
        return [cappuccino_cup_cost, -cappuccino_water_quantity, -cappuccino_milk_quantity, -cappuccino_beans_quantity,
                -1]

    @staticmethod
    def _transform_resource_number(resource_number):
        if resource_number == 1:
            return 'water'
        elif resource_number == 2:
            return 'milk'
        elif resource_number == 3:
            return 'bean'
        elif resource_number == 4:
            return 'disposable_cups'
        else:
            return ''

    def __init__(self, c_money, c_water_margin, c_milk_margin, c_bean_margin, c_disposable_cups):
        self.money = c_money
        self.water_margin = c_water_margin
        self.milk_margin = c_milk_margin
        self.bean_margin = c_bean_margin
        self.disposable_cups = c_disposable_cups
        self.state = 'choosing an action'

    def run(self):
        while True:
            print('Write action (buy, fill, take, remaining, exit):')
            user_action = input().strip()
            if user_action == 'exit':
                break
            self.process_user(user_action)

    def process_user(self, input_string):
        if self.state == 'choosing an action':
            if input_string == 'take':
                self.take_money()
            elif input_string == 'buy':
                self.state = 'choosing a type of coffee'
                self.buy_coffee()
                self.state = 'choosing an action'
            elif input_string == 'fill':
                self.fill_resource()
            elif input_string == 'remaining':
                self.print_resource()
        elif self.state == 'choosing a type of coffee':
            self.buy_coffee()
            self.state = 'choosing an action'

    def buy_coffee(self):
        print('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino:')
        choice = input().strip()
        if choice == 'back':
            return None
        if choice in ['1', '2', '3']:
            choice = int(choice)
            _subtract_list = [self._espresso_unit_subtract, self._latte_unit_subtract, self._cappucino_unit_subtract]
            answer = self._transform_resource_number(self.get_ingredient_availability(choice))
            if answer == '':
                self.recount_resources(_subtract_list[choice - 1]())
                print('I have enough resources, making you a coffee!')
            else:
                print('Sorry, not enough', answer + '!')
            return None

    def recount_resources(self, args_list):
        self.money += args_list[0]
        self.water_margin += args_list[1]
        self.milk_margin += args_list[2]
        self.bean_margin += args_list[3]
        self.disposable_cups += args_list[4]

    def get_ingredient_availability(self, resource_number):
        _subtract_functions = [self._espresso_unit_subtract, self._latte_unit_subtract, self._cappucino_unit_subtract]
        temp_list = _subtract_functions[resource_number - 1]()
        for i, resource in enumerate([self.water_margin, self.milk_margin, self.bean_margin, self.disposable_cups]):
            if resource + temp_list[i + 1] < 0:
                return i + 1
        return 0

    def fill_resource(self):
        print('Write how many ml of water do you want to add:')
        added_water = int(input().strip())
        print('Write how many ml of milk do you want to add:')
        added_milk = int(input().strip())
        print('Write how many grams of coffee beans do you want to add:')
        added_bean = int(input().strip())
        print('Write how many disposable cups of coffee do you want to add:')
        added_disposable_cups = int(input().strip())
        self.recount_resources([0, added_water, added_milk, added_bean, added_disposable_cups])

    def take_money(self):
        print('I gave you $' + str(self.money))
        self.recount_resources([-self.money, 0, 0, 0, 0])

    def print_resource(self):
        print('The coffee machine has:'
              + '\n', self.water_margin, 'of water'
              + '\n', self.milk_margin, 'of milk'
              + '\n', self.bean_margin, 'of coffee beans'
              + '\n', self.disposable_cups, 'of disposable cups'
              + '\n', self.money, 'of money')


# Write your code here
print('''
Starting to make a coffee
Grinding coffee beans
Boiling water
Mixing boiled water with crushed coffee beans
Pouring coffee into the cup
Pouring some milk into the cup
Coffee is ready!
''')

coffee_machine = CoffeeMachine(550, 400, 540, 120, 9)
coffee_machine.run()
