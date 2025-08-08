
class FewShotExamples:
    def examples(self, doctype: str):
        """
        Return a list of example docstrings for functions or classes.
        
        Parameters
        ----------
        doctype : str
            The type of docstrings to retrieve. Should be either 'function' or 'class'.
        
        Returns
        -------
        list
            A list of example docstrings for functions or classes based on the input type.
        """
        docstrings = []
        code = []
        if doctype.startswith('function') or doctype.startswith('method_declaration'):
            code = [
                """
                def bubble_sort(arr):
                    
                    # Outer loop to iterate through the list n times
                    for n in range(len(arr) - 1, 0, -1):
                        
                        # Initialize swapped to track if any swaps occur
                        swapped = False  

                        # Inner loop to compare adjacent elements
                        for i in range(n):
                            if arr[i] > arr[i + 1]:
                            
                                # Swap elements if they are in the wrong order
                                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                                
                                # Mark that a swap has occurred
                                swapped = True
                        
                        # If no swaps occurred, the list is already sorted
                        if not swapped:
                            break
                """,

                """
                public static String reverse(String input) {
                    String reversed = "";
                    for (int i = input.length() - 1; i >= 0; i--) {
                        reversed += input.charAt(i);
                    }
                    return reversed;
                }

                """,
                """
                def get_domain_name(ip_address):
                    try:
                        hostname = socket.gethostbyaddr(ip_address)[0]
                        return hostname
                    except socket.herror:
                        return "No domain name found"
                """
            ]

            docstrings = [
                {
                    "description": "Sorts an array using the bubble sort algorithm.",
                    "parameters": 
                    {
                        "name": "arr", 
                        "description": "The list to be sorted."
                    },
                     "returns": 
                    {
                        "description": "None."
                    },
                },
                {
                    "description": "Reverse the characters in a given string.",
                    "parameters": 
                        {
                            "name": "input_string",
                            "description": "The input string to be reversed."
                         },
                    "returns": {
                        "type": "str",
                        "description": "The reversed string."
                    }
                },
                {
                    "description": "Get the DNS name (hostname) associated with an IP address.",
                    "parameters": 
                        {
                            "name": "ip_address",
                            "description": "The IP address for which to find the corresponding DNS name."
                         },
                    
                    "returns": {
                        "type": "str",
                        "description": "The DNS name associated with the IP address. If no DNS name is found, returns an error message."
                    },
                }
            ]
        if doctype.startswith('rule'):
            code = [
                """
                help:
                    @awk 'BEGIN {FS = ":.*"; printf "\\nUsage:\\n  make \\033[36m<target>\\033[0m\\n"} /^[a-zA-Z_-]+:.*##/ { printf "  \\033[36m%-15s\\033[0m %s\\n", $$1, $$2 } /^#@@/ { prev_desc = substr($$0, 4) } /^[a-zA-Z_-]+:/ { if (prev_desc != "") { printf "  \\033[36m%-15s\\033[0m %s\\n", $$1, prev_desc; prev_desc = "" } }' $(MAKEFILE_LIST)
                """,
                """
                help-%:
                    @awk -v rule=$* 'BEGIN {FS = ":.*"; found=0 } /^#@/ { prev_desc = substr($$0, 4) } \\
                    /^[a-zA-Z_-]+:/ && $$1 == rule { \\
                        if (prev_desc != "") { \\
                            printf "\\nDocumentation for \\033[36m`%s`\\033[0m rule:\\n\\n", rule; \\
                            printf "%s\\n", prev_desc; \\
                            found=1; \\
                            prev_desc = "" } }END { if (!found) printf "No documentation found for \\033[36m`make %s`\\033[0m\\n", rule }' $(MAKEFILE_LIST)                
                """,
                """
                .%.d:%.cc
                    @echo -n $(dir $<) > $@
                    @$(DEPEND.d) $< >> $@
                """
            ]


            docstrings = [
                {
                    "short_description": "Generates a short help message for the makefile targets.",
                    "long_description": "This code uses awk to parse the makefile and generate a help message for the available targets. It prints the usage and a list of targets with their descriptions.",
                },
                {
                    "short_description": "Generates a long help message for the makefile targets.",
                    "long_description": "The code uses awk to parse the makefile and display help information for the specified target. It looks for lines starting with #@ to extract the description for the target. If the target is found, it prints the help information; otherwise, it displays a message indicating that no documentation was found for the specified target.",
                },
                {
                    "short_description": "Generates a dependency file for the given source file.",
                    "long_description": "This code snippet uses a makefile rule to generate a dependency file for the given source file. It extracts the directory of the source file and appends the dependency information to the target file.",
                },


            ]
        if doctype.startswith('class'):
            code = [
                """
                class Person:
                    def __init__(self, name, surname, age):
                        self.name = name
                        self.surname = surname
                        self.age = age

                    def info(self, additional=""):
                        print(f'My name is {self.name} {self.surname}. I am {self.age} years old.' + additional)
                """,

                """
                class Employee:
                    def __init__(self, name, age, department, salary):
                        self.name = name
                        self.age = age
                        self.department = department
                        self.salary = salary

                    def promote(self, raise_amount):
                        self.salary += raise_amount
                        return f"{self.name} has been promoted! New salary: ${self.salary:.2f}"

                    def retire(self):
                        return f"{self.name} has retired. Thank you for your service!"

                """,

                """
                class CreateBIWorkflow(BaseWorkflow):
                    def create_customer_record(self, customer_info):
                        exists = self.db.exists_document(index=self.env_conf["customer_table"], doc_id=customer_info["cust-id"])
                        if not exists:
                            self.db.create_document(index=self.env_conf["customer_table"], body=customer_info, doc_id=customer_info["cust-id"])

                    def create_vpn_template(self, customer_info):
                        vpn_record = {"bi-service":[{}]}
                        bi_service = vpn_record["bi-service"][0]
                        bi_service["cloud-accesses"] = {"cloud-access":[{"cloud-identifier": "TELUS_BI_MPLS"}]}
                        bi_service["customer-name"] = customer_info["cust-shortname"]
                        bi_service["telus-cust-info"] = {"cust-id": customer_info["cust-id"]}
                        vpn_id = bi_service["customer-name"] + "-BI-MPLS"
                        bi_service["vpn-id"] = vpn_id
                        bi_service["state"] = "INACTIVE"
                        bi_service["sites"] = {"site": []}

                        return vpn_id, vpn_record

                    def execute(self, nb_request_payload, audit=False):
                        exec_med_payload = {}
                        exec_med_id = exec_med_uri = ""
                        request_type = RequestType.CREATE_VPN
                        try:
                            logger.info("Inside instantiate method to create a BI service")
                            request_data = nb_request_payload["request-characteristics"]["payload"]
                            nb_site_payload = request_data["serviceCharacteristic"][0]["value"]["site"]
                            customer_info = nb_site_payload["telus-cust-info"]
                            devices = self.extract_pe_devices(nb_site_payload)
                            doc_id, result = self.lookup_vpn_by_id(id=customer_info["cust-id"], id_type="customer")
                            vpn_id = ""
                            if not doc_id:
                                logger.info("No vpn found for customer {0}".format(customer_info["cust-id"]))
                                self.create_customer_record(customer_info)
                                vpn_id, vpn_record = self.create_vpn_template(customer_info)
                                logger.info("VPN id of the newly created vpn: {0}".format(vpn_id))
                            else:
                                vpn_record = result
                                vpn_id = vpn_record["bi"]["mpls"]["bi-services"]["bi-service"][0]["vpn-id"]
                                logger.info("VPN Id of the existing VPN: {0}".format(vpn_id))

                            transformed_site = self.transformer.transform_site(nb_site_payload, vpn_id)
                            site_id = transformed_site["site-id"]
                            entity_name = "{0}_{1}".format(vpn_id, site_id)

                            if not doc_id:
                                request_type = RequestType.CREATE_VPN
                                data_model_path = "/yang/bi/mpls/bi-services"
                                exec_med_uri = self.env_conf["executor_activate_uri"] + data_model_path
                                vpn_site_list = vpn_record["bi-service"][0]["sites"]["site"]
                                vpn_site_list.append(transformed_site)
                                exec_med_payload = self.make_executor_payload(entity_name=entity_name, model_name=self.env_conf["executor_model_name"], model_revision=self.env_conf["executor_model_revision"], payload=vpn_record)
                                exec_med_id = self.call_executor(method='post', exec_med_uri=exec_med_uri, exec_med_payload=exec_med_payload, devices=devices, audit=audit)
                            else:
                                request_type = RequestType.CREATE_SITE
                                data_model_path = "/yang/bi/mpls/bi-services/bi-service={}/sites".format(vpn_id)
                                exec_med_uri = self.env_conf["executor_activate_uri"] + data_model_path
                                payload = {"site": transformed_site}
                                exec_med_payload = self.make_executor_payload(entity_name=entity_name, model_name=self.env_conf["executor_model_name"], model_revision=self.env_conf["executor_model_revision"], payload=payload)
                                exec_med_id = self.call_executor(method='post', exec_med_uri=exec_med_uri, exec_med_payload=exec_med_payload, devices=devices, audit=audit)
                        
                        except ExecutorTooManyRequests as e:
                            self.inform_northbound(request_tracker_payload=nb_request_payload, status="error", request_type=request_type.value,
                                                                        reason=[e.message], error_code=e.error_code)
                        
                        except Exception as e:
                            logger.exception(e)
                            reason = ["Internal server error"]
                            self.inform_northbound(request_tracker_payload=nb_request_payload, request_type=request_type.value,
                                                                        status="error", reason=reason, error_code="ERR201")
                        
                        finally:
                            self.store_request_tracker(nb_request_payload=nb_request_payload, exec_med_payload=exec_med_payload, method_type='POST',
                                                    exec_med_uri=exec_med_uri, exec_med_id=exec_med_id, request_type=request_type)
                """
            ]

            docstrings = [
                {
                    "description": "A class to represent a person.",
                    "attributes": [
                        {"name": "name", "description": "first name of the person"},
                        {"name": "surname", "description": "family name of the person"},
                        {"name": "age",  "description": "age of the person"},
                    ]
                },
                {
                    "description": "A class representing an employee",
                    "attributes": [
                        {"name": "name", "description": "The name of the employee."},
                        {"name": "age", "description": "The age of the employee."},
                        {"name": "department", "description": "The department the employee works in."},
                        {"name": "salary", "description": "The salary of the employee."}
                    ]
                },
                {
                    "description": "Class for creating and managing BI workflow for customer records and VPN templates."
                },
                # {
                #     "description": "Handler class to process health check requests."
                # }

            ]
        if doctype == 'statemachine':
            code = [
                """
                statemachine {
                    state Thinking {
                        entry
                        `
                            std::cout  << myName << " thinking" << std::endl;
                            timerP.informIn(RTTimespec(2,100000000));
                        `;
                    }, Wait4Right, Wait4Left, Wait4First, GoLeftWait4Right, GoRightWait4Right, Eating {
                        entry
                        `
                            std::cout << "                                         " << myName  << " eating" << std::endl;

                            int rnd = rand() % 10;
                            timerP.informIn(RTTimespec(0,rnd*10000000));
                        `;
                    };
                    choice _junction;
                    _initial: initial -> Thinking
                    `
                        // read in the initialization arguments
                        PhilArgs pArgs = (PhilArgs) *((PhilArgs*) rtdata);

                        id = pArgs.id;
                        numPhils = pArgs.numPhils;
                        pickUpStrat = pArgs.pickUpStrat;

                        // my name is 'phil'+id
                        char buffer1[10];
                        snprintf(buffer1, 10, "phil%d", id);            
                        myName = new char[strlen(buffer1) + 1];
                        strcpy(myName, buffer1);
                        std::cout<< myName << " starting up "  << std::endl;

                        // initialize random number generator
                        srand(time(NULL));
                    `;
                    gotTimeout: Thinking -> _junction on timerP.timeout;
                    left_first: _junction -> Wait4Left when
                    `
                        return (pickUpStrat==PickUpStrategy::LEFTFIRST);`
                    `
                        leftP.up().send();
                    `;
                    right_first: _junction -> Wait4Right when
                    `
                        return (pickUpStrat==PickUpStrategy::RIGHTFIRST);`
                    `
                        rightP.up().send();
                    `;
                    random: _junction -> Wait4First when
                    `
                        return (pickUpStrat==PickUpStrategy::RANDOM);
                    `
                    `
                        int rnd = rand() % 100;
                        if (rnd>50) 
                            leftP.up().send();
                        else 
                            rightP.up().send();
                    `;
                    random_else: _junction -> Wait4First when `else`;
                    gotLeft1: Wait4Left -> GoLeftWait4Right on leftP.ack
                    `
                        std::cout << "                                         " << myName << " got left " << std::flush << std::endl;
                        rightP.up().send();
                    `;
                    gotLeft2: Wait4First -> GoLeftWait4Right on leftP.ack
                    `
                        std::cout<< "                                         " << myName << " got left "  << std::flush << std::endl;
                        rightP.up().send();
                    `;
                    gotRight1: Wait4Right -> GoRightWait4Right on rightP.ack
                    `
                        std::cout << "                                         "<< myName  << " got right " << std::flush << std::endl;
                        leftP.up().send();
                    `;
                    gotRight2: Wait4First -> GoRightWait4Right on rightP.ack
                    `
                        std::cout << "                                         "<< myName << " got right " << std::flush << std::endl;
                        leftP.up().send();
                    `;
                    gotLeft3: GoRightWait4Right -> Eating on leftP.ack
                    `
                        // std::cout  << myName << " to eating 1 " << std::flush << std::endl;
                    `;
                    gotRight3: GoLeftWait4Right -> Eating on rightP.ack
                    `
                        // std::cout << myName << " to eating 2 "  << std::flush << std::endl;
                    `;
                    putDownForks: Eating -> Thinking on timerP.timeout
                    `
                        leftP.down().send();
                        rightP.down().send();
                    `;

                };

                """,
                """
                statemachine {
                    state S1, S2;
                    initial -> S1
                    `
                        RTTimerId tid = timer.informIn(RTTimespec(2, 0));
                        if (!tid.isValid()) {
                            // timer could not be set
                        }
                    `;
                    S1 -> S2 on timer.timeout
                    `
                        std::cout << "Hello World!" << std::endl;
                        context()->abort();
                    `;
                };
                """,
                """
                    statemachine {
                    };
                """,
                """
                statemachine {

                    state  State2 {
                        entry `
                            timing.informIn(RTTimespec(0,500000000)); // 0.5 s
                        `;
                        timeout: on timing.timeout `
                            count++;
                            p.ping().send();
                        `;
                    }, Done2 {
                        entry `
                            std::cout << "Done!" << std::endl;
                        `;
                    };
                    choice choice2;
                    redefine _initial: initial -> State2 `
                        std::cout << "Fast Pinger initialized!" << std::endl << std::flush;;
                    `;
                    result2: State2 -> choice2 on p.result;
                    else2: choice2 -> Done2 when `else`;
                    false2: choice2 -> State2 when `return count < 10;`;
                };
                """
            ]
            docstrings = [
                {
                    'pseudostates': [{'name': 'initial', 'type': 'initial', 'description': 'The starting point of the state machine.'},
                        {'name': '_junction', 'type': 'choice', 'description': 'A decision point used for branching transitions based on conditions. Used to decide which fork to pick up first based on the `pickUpStrat` strategy. Handles randomized selection if the strategy is `RANDOM`.'}], 
                    'states': [{'name': 'Thinking', 'description': 'Philosopher is thinking and sets a timer before attempting to pick up forks.'}, 
                               {'name': 'Wait4Right', 'description': 'Waiting for the right fork after initiating a pickup request.'}, 
                               {'name': 'Wait4Left', 'description': 'Waiting for the left fork after initiating a pickup request.'}, 
                               {'name': 'Wait4First', 'description': 'Randomized waiting for either fork depending on strategy.'}, 
                               {'name': 'GoLeftWait4Right', 'description': 'Acquired left fork, now waiting for right fork.'}, 
                               {'name': 'GoRightWait4Right', 'description': 'Successfully acquired both forks; eating for a randomized duration.'}, 
                               {'name': 'Eating', 'description': 'State for eating and setting timer for next action'}], 
                    'transitions': [{'name': 'gotTimeout', 'source': 'Thinking', 'target': '_junction', 'description': 'Timeout reached; decide pickup strategy.'}, 
                                    {'name': 'left_first', 'source': '_junction', 'target': 'Wait4Left', 'description': 'Transition based on pickUpStrat. Pickup strategy is LEFTFIRST.'}, 
                                    {'name': 'right_first', 'source': '_junction', 'target': 'Wait4Right', 'description': 'Transition based on pickUpStrat. Pickup strategy is RIGHTFIRST.'}, 
                                    {'name': 'random', 'source': '_junction', 'target': 'Wait4First', 'description': 'Randomly pick a fork to request first.'}, 
                                    {'name': 'random_else', 'source': '_junction', 'target': 'Wait4First', 'description': 'If no specific strategy is set, default to waiting for a random fork.'}, 
                                    {'name': 'gotLeft1', 'source': 'Wait4Left', 'target': 'GoLeftWait4Right', 'description': 'Transition on receiving left fork; request right fork'}, 
                                    {'name': 'gotLeft2', 'source': 'Wait4First', 'target': 'GoLeftWait4Right', 'description': 'Transition on receiving left fork; request right fork'}, 
                                    {'name': 'gotRight1', 'source': 'Wait4Right', 'target': 'GoRightWait4Right', 'description': 'Transition on receiving right fork; request left fork'}, 
                                    {'name': 'gotRight2', 'source': 'Wait4First', 'target': 'GoRightWait4Right', 'description': 'Transition on receiving right fork; request left fork'}, 
                                    {'name': 'gotLeft3', 'source': 'GoRightWait4Right', 'target': 'Eating', 'description': 'Transition on receiving left fork; start eating.'}, 
                                    {'name': 'gotRight3', 'source': 'GoLeftWait4Right', 'target': 'Eating', 'description': 'Transition on receiving right fork; start eating.'}, 
                                    {'name': 'putDownForks', 'source': 'Eating', 'target': 'Thinking', 'description': 'After finishing a meal, release forks and return to thinking.'}], 
                    'summary': 'State machine for a dining philosopher problem simulation', 
                    'long_description': "This state machine models a philosopher's behavior in acquiring forks and transitioning between thinking and eating. Philosophers follow different fork-picking strategies (LEFTFIRST, RIGHTFIRST, RANDOM) to reduce the likelihood of deadlock.", 
                    'language': 'art', 
                    'doc_type': 'artdoc'
                },

                {
                    'pseudostates': [{'name': 'Initial', 'type': 'initial', 'description': 'The starting point of the state machine.'}], 
                    'states': [{'name': 'S1', 'description': 'State where a timer is started and we are waiting for it to timeout.'}, 
                               {'name': 'S2', 'description': 'The final state where a message is printed when the timer runs out, and the process is aborted.'}], 
                    'transitions': [{'name': 'Initial', 'source': 'Initial', 'target': 'S1', 'description': 'Initializes the timer to trigger after 2 seconds.'}, 
                                    {'name': 'gotTimeout', 'source': 'S1', 'target': 'S2', 'description': 'When the timer expires, prints "Hello World!" and terminates the process.'}], 
                    'summary': 'Simple State Machine for Hello World example', 
                    'long_description': "This state machine demonstrates a basic timed transition between states. It sets a timer upon entering the initial state and transitions to the next state when the timer expires.", 
                    'language': 'art', 
                    'doc_type': 'artdoc'
                },
                {
                    'summary': 'Empty State Machine' 
                },
                {
                    'pseudostates': [{'name': '_initial', 'type': 'initial', 'description': 'Initialization message for the state machine.'},
                                     {'name': 'choice2', 'type': 'choice', 'description': 'Decision point based on the result of the ping.'}], 
                    'states': [{'name': 'S1', 'description': 'State where a timer is started and we are waiting for it to timeout.'}, 
                               {'name': 'S2', 'description': 'The final state where a message is printed when the timer runs out, and the process is aborted.'}], 
                    'transitions': [{'name': 'timeout', 'source': 'State2', 'target': 'State2', 'description': 'Increment count and send ping on timeout.'}, 
                                    {'name': 'result2', 'source': 'State2', 'target': 'choice2', 'description': 'Transition based on the result of the ping.'},
                                    {'name': 'false2', 'source': 'choice2', 'target': 'State2', 'description': 'Return to State2 if count is less than 10.'},
                                    {'name': 'else2', 'source': 'choice2', 'target': 'Done2', 'description': 'Transition to Done2 if no other conditions are met.'}], 
                    'summary': 'State machine for managing timing and ping operations ', 
                    'long_description': "This state machine handles timing and ping operations, transitioning between State2 and Done2 based on the result of the ping and the count value. ", 
                    'language': 'art', 
                    'doc_type': 'artdoc'
                },
            ]
        return docstrings, code