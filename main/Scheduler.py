import pandas

from Workstate import Workstate
from Inspector import Inspector
from Buffer import Buffer
from ComponentType import ComponentType
from Log import log
from Workstation import Workstation
from ProductType import ProductType
from RandomGen import exp_rand_gen_range

# Temp Import for Testing

# Author: James
SIMULATIONTIME = 3000


class Scheduler:
    eventList = []
    time = -1

    productsMade = 0

    entities = []

    def __init__(self):
        self.eventList = []
        self.time = 0

    def addEvent(self, new):
        self.eventList.append(new)
        self.sortEvents()

    def getTime(self, e):
        return e.time

    def setTime(self, new):
        self.time = new

    def sortEvents(self):
        self.eventList.sort(key=self.getTime)

    def idleCheck(self):
        checks = 0
        log("Time is at: " + str(self.time) + ", Checking Idle Entities")
        active = 0
        for i in self.entities:
            checks += 1
            if i.state == Workstate.IDLE:
                i.activate()
                active += 1
        log("     " + str(checks) + " entites checked for idleness")
        log("     " + str(active) + " entites have been activated")
        return

    def popEvent(self):
        if len(self.eventList) == 0:
            log("There exists no Events to Process")
            return -1
        x = self.eventList.pop(0)
        return x


def main():
    # Create the Scheduler
    schedule = Scheduler()

    # Creating the Queues
    # Name Format: QC#W#
    # Explanation
    #   C# references the component the queue accepts
    #   W# references which workstation uses the queue
    QC1W1 = Buffer()
    QC1W2 = Buffer()
    QC1W3 = Buffer()

    QC2W2 = Buffer()

    QC3W3 = Buffer()

    # Creating random times
    num_samples = 300
    i1_c1_rand = exp_rand_gen_range(10.35791, 0.087, 76.284, num_samples)
    i2_c2_rand = exp_rand_gen_range(15.58843, 0.13, 114.43, num_samples)
    i2_c3_rand = exp_rand_gen_range(20.63276, 0.031, 104.02, num_samples)
    ws1_rand = exp_rand_gen_range(4.604417, 0.007, 29.375, num_samples)
    ws2_rand = exp_rand_gen_range(10.93212, 0.091, 59.078, num_samples)
    ws3_rand = exp_rand_gen_range(8.79558, 0.102, 51.418, num_samples)

    # Create the Entities
    #   Creating the Inspectors
    I1 = Inspector([QC1W1, QC1W2, QC1W3], ComponentType.C1, schedule, i1_c1_rand)
    I2 = Inspector([QC2W2, QC3W3], [ComponentType.C2, ComponentType.C3], schedule, [i2_c2_rand, i2_c3_rand])

    #   Creating the Workstations
    W1 = Workstation([QC1W1], ProductType.P1, schedule, ws1_rand)
    W2 = Workstation([QC1W2, QC2W2], ProductType.P2, schedule, ws2_rand)
    W3 = Workstation([QC1W3, QC3W3], ProductType.P3, schedule, ws3_rand)

    # Add Inspectors to Scheduler
    schedule.entities.append(I1)
    schedule.entities.append(I2)
    schedule.entities.append(W1)
    schedule.entities.append(W2)
    schedule.entities.append(W3)

    # Add Initial events(Via the Idle Check)
    schedule.idleCheck()
    # Simulation loop
    code = 1
    while code != -1:
        # Go to next event
        x = schedule.popEvent()
        # temp code to handle having no events
        if x == -1 or schedule.time > SIMULATIONTIME:
            code = -1
        else:
            if x.time == -1:
                break
            else:
                x.handle()
                schedule.setTime(x.time)
        # Checking if any of the idle entities can fire
        schedule.idleCheck()

    log("Simulation Ended at Time: " + str(schedule.time))
    log("REPORT:")
    log(" Production:")
    log("   Workstation W1 Produced: " + str(len(W1.products)) + " units P1")
    log("   Workstation W2 Produced: " + str(len(W2.products)) + " units P2")
    log("   Workstation W3 Produced: " + str(len(W3.products)) + " units P3")
    log(" Time Blocked:")
    log("   Inspector I1 Blocked for: " + str(I1.timeBlocked) + " Units Time")
    log("   Inspector I2 Blocked for: " + str(I2.timeBlocked) + " Units Time")
    log("   Workstation W1 Blocked for: " + str(W1.timeBlocked) + " Units Time")
    log("   Workstation W2 Blocked for: " + str(W2.timeBlocked) + " Units Time")
    log("   Workstation W3 Blocked for: " + str(W3.timeBlocked) + " Units Time")

    log("Random Values remaining:")
    log("Inspector 1, Component 1: " + str(len(I1.randDurations)))
    log("Inspector 2, Component 2: " + str(len(I2.randDurations[0])))
    log("Inspector 2, Component 3: " + str(len(I2.randDurations[1])))
    log("Workstation 1: " + str(len(W1.randDurations)))
    log("Workstation 2: " + str(len(W2.randDurations)))
    log("Workstation 3: " + str(len(W3.randDurations)))

    #Process report summary
    log('Generating Report File')
    report_dict = {
        'Workstation 1 Products': [str(len(W1.products))],
        'Workstation 2 Products': [str(len(W2.products))],
        'Workstation 3 Products': [str(len(W3.products))],
        'Inspector 1 Blocked Time': [str(I1.timeBlocked)],
        'Inspector 2 Blocked Time': [str(I2.timeBlocked)],
        'Workstation 1 Blocked Time': [str(W1.timeBlocked)],
        'Workstation 2 Blocked Time': [str(W1.timeBlocked)],
        'Workstation 3 Blocked Time': [str(W1.timeBlocked)],
    }
    report_df = pandas.DataFrame.from_dict(report_dict)
    report_df.to_csv('report_summary.csv')

    #Process input info
    log('Generating Input File')
    input_dict = {
        'Inspector 1 C1': i1_c1_rand,
        'Inspector 2 C2': i2_c2_rand,
        'Inspector 2 C3': i2_c3_rand,
        'Workstation 1': ws1_rand,
        'Workstation 2': ws2_rand,
        'Workstation 3': ws3_rand
    }
    input_df = pandas.DataFrame.from_dict(input_dict)
    input_df.to_csv('rand_inputs.csv')

    #Process Workstation 1 info
    log('Generating Workstation 1 File')
    w1_dict = {
        'C1 Arrival Time': [],
        'Product 1 Finish Time': [],
    }
    for product in W1.products:
        w1_dict['Product 1 Finish Time'].append(product.get_create_time())
        for component in product.components:
            if component.get_component_type() == ComponentType.C1:
                w1_dict['C1 Arrival Time'].append(component.get_create_time())
    w1_df = pandas.DataFrame.from_dict(w1_dict)
    w1_df.to_csv('workstation_1.csv')

    # Process Workstation 2 info
    log('Generating Workstation 2 File')
    w2_dict = {
        'C1 Arrival Time': [],
        'C2 Arrival Time': [],
        'Product 2 Finish Time': [],
    }
    for product in W2.products:
        w2_dict['Product 2 Finish Time'].append(product.get_create_time())
        for component in product.components:
            if component.get_component_type() == ComponentType.C1:
                w2_dict['C1 Arrival Time'].append(component.get_create_time())
            elif component.get_component_type() == ComponentType.C2:
                w2_dict['C2 Arrival Time'].append(component.get_create_time())
    w2_df = pandas.DataFrame.from_dict(w2_dict)
    w2_df.to_csv('workstation_2.csv')

    # Process Workstation 3 info
    log('Generating Workstation 3 File')
    w3_dict = {
        'C1 Arrival Time': [],
        'C3 Arrival Time': [],
        'Product 3 Finish Time': [],
    }
    for product in W3.products:
        w3_dict['Product 3 Finish Time'].append(product.get_create_time())
        for component in product.components:
            if component.get_component_type() == ComponentType.C1:
                w3_dict['C1 Arrival Time'].append(component.get_create_time())
            elif component.get_component_type() == ComponentType.C3:
                w3_dict['C3 Arrival Time'].append(component.get_create_time())
    w3_df = pandas.DataFrame.from_dict(w3_dict)
    w3_df.to_csv('workstation_3.csv')


    input("---Press any Button to Exit---")


if __name__ == "__main__":
    main()
