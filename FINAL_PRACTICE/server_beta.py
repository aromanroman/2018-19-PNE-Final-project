# This is the server for the final practice.
import http.server
import socketserver
import termcolor
import http.client
import json
from Seq import Seq

PORT = 8000


class TestHandler(http.server.BaseHTTPRequestHandler):

    # This is a function very useful with this function we can get the keys(values of the buttons on the web page)
    # and its correspondent values that will depend on the information introduced by the user

    def manage_arguments(self, path):
        argument_dictionary = dict()
        print(argument_dictionary)
        if "?" in path:
            arguments = self.path.split("?")[1]
            arguments = arguments.split(" ")[0]
            print(arguments)
            pieces = arguments.split("&")
            print(pieces)
            for b in pieces:
                if '=' in b:
                    key = b.split("=")[0]
                    print(key)
                    value = b.split("=")[1]
                    print(value)
                    argument_dictionary[key] = value
        print(argument_dictionary)
        return argument_dictionary

    def do_GET(self):
        status = 200
        json_response = False
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""
        termcolor.cprint(self.requestline, 'green')
        # if the self path only have: / , it will show the web page created(index.html)
        if self.path == "/":
            with open("index.html", "r") as f:
                contents = f.read()
        # Now the self path will have many parts depending on the information introduced in the boxes.
        # So we will called the manage_argument function in order to get the keys with the correspondent value,
        # if we do this we get that if someone introduces directly the self path with the keys in different order
        # could receive the information required ()

        elif 'listSpecies' in self.path:
            arguments = self.manage_arguments(self.path)
            print(arguments)
            if 'limit' in arguments:
                try:
                    limit = int(arguments["limit"])
                # with the exception ValueError we get that if the limit introduced is not digit the page did not fall.
                # We decided to introduce limit = 0 in case of this exception due to a few lines after this one,
                # we can see that if the limit = 0 the server wil sent the list of all species with no limit
                except ValueError:
                    limit = 0
                    status = 404
            # if you do not introduce a limit automatically we stablish limit=0,
            # and server will send the list of all species

            else:
                limit = 0
            conn = http.client.HTTPConnection("rest.ensembl.org")
            conn.request("GET", "/info/species?content-type=application/json")
            r1 = conn.getresponse()
            print()
            print("Response received: ", end='')
            print(r1.status, r1.reason)
            text_json = r1.read().decode("utf-8")
            response = json.loads(text_json)
            conn.close()
            print(response)
            list_species = response["species"]
            print("LIST", list_species)
            json_variable_message = ""
            contents2 = ""
            contents3 = ""
            # Now we are going to manage the different possibilities of the limit introduced
            try:
                # the first possibility is when the limit is superior to the length of the list of species,
                # in this case the server will send the complete list of all species,
                # this also will be sent if the limit==0.
                # The difference is the message that tell us the cause (json_variable_message, contents)
                # I prepare the information in case that the format was json or not at the same time,
                # in order not to spend a lot of lines.

                if limit > len(list_species) or limit == 0:
                    if limit > len(list_species):
                        # The line was too long and it was marked as a mistake,
                        # so I fractioned the message in two phrases and then summarize it.
                        contents2 = "You introduced a limit number superior to the total length of the list of species."
                        contents3 = "So you will get the completely list of the species:"
                        json_variable_message1 = "limit number superior to the total length of the list of species."
                        json_variable_message = json_variable_message1 + " You get the whole list"
                    elif limit == 0:
                        contents2 = "You introduced incorrectly the limit. "
                        contents3 = "So you will get the completely list of the species:"
                        json_variable_message = "limit number introduced incorrectly. You get the whole list"
                    species_limit = list_species[:len(list_species)]
                # Now we see if the limit introduced is correct
                else:
                    contents2 = "The list with the limit {} introduced is: ".format(limit)
                    contents3 = ""
                    species_limit = list_species[:limit]
                    json_variable_message = "You introduced correctly the limit. You will get list with the limit"
                    print("the limit is", species_limit)
            # The KeyError exception is god, it will help us if the limit is not introduced.
            except KeyError:
                print("sorry you had not introduced a limit")
                species_limit = list_species[:len(list_species)]
                status = 404
            # Now we manage if the json is in self path, i have testing and if is not selected,
            # it does not appear in the self path so I just write the following if:
            if "json" in arguments:
                # The variable json_response will help us later and its function is to communicate to the server,
                # that the client wants the response in json format
                json_response = True
                contents = json.dumps([{"message from the server: ": json_variable_message}, species_limit])
            # if json is not in argument, means that the checkbox of json is not selected and that the client want
            # the response in html format
            else:
                contents = """
                    <ol type= "i">
                     <html>
                     <body>
                     """
                contents += contents2 + contents3
                for n in species_limit:
                    contents = contents + "<li>" + n["display_name"] + "</li>"
                contents = contents + """
                </ol> 
                </body>
                </html>
                """
        # Now the next elifs will be explained less than the first one, due to many things are already explained
        elif "karyotype" in self.path:
            try:
                arguments = self.manage_arguments(self.path)
                # I will check if the specie is introduced but also if the value of the specie key is not empty
                if "specie" in arguments and arguments['specie'] != "":
                    specie = arguments["specie"]
                    if "+" in specie:
                        specie = specie.replace("+", "_")


                    conn = http.client.HTTPConnection("rest.ensembl.org")
                    conn.request("GET", "/info/assembly/" + specie + "?content-type=application/json")
                    r1 = conn.getresponse()
                    data1 = r1.read().decode("utf-8")
                    response = json.loads(data1)
                    print(response)
                    list_chromo = response["karyotype"]
                    print(list_chromo)
                    if "json" in arguments:
                        json_response = True
                        json_response = [specie, {"Karyotype": list_chromo}]
                        contents = json.dumps(json_response)
                    else:
                        contents = """
                             <html>
                             <body>
                             <ul>"""
                        # the next "for" is very useful for introducing correctly the chromosomes in html format
                        # "<li>" in html format is for having an enummerate list with roman numbers.
                        if len(list_chromo) > 0:
                            for chromo in list_chromo:
                                contents = contents + "<li>" + chromo + "</li>"
                        elif len(list_chromo) == 0:
                            contents += "The specie has no karyotype"

                        contents = contents + """
                        </ul> 
                        </body>
                        </html>
                        """

                    print("the contests are:", contents)
                else:
                    if "json" in self.path:
                        json_response = True
                        msg = "message from the server"
                        json_response = {msg: "you introduced a specie that is wrong or that is not in the data base"}
                        contents = json.dumps(json_response)
                    else:
                        contents = """
                                                                     <html>
                                                                     <body>
                                                                     <ul>"""
                        contents = "you introduced a specie that is wrong or that is not in the data base"
                        contents = contents + """
                                                                </ul> 
                                                                </body>
                                                                </html>
                                                                """

            except KeyError:

                if "json" in self.path:
                    json_response = True
                    msg = "message from the server"
                    json_response = {msg: "you introduced a specie that is wrong or that is not in the data base"}
                    contents = json.dumps(json_response)
                else:
                    contents = """
                                                                 <html>
                                                                 <body>
                                                                 <ul>"""
                    contents = "you introduced a specie that is wrong or that is not in the data base"
                    contents = contents + """
                                                            </ul> 
                                                            </body>
                                                            </html>
                                                            """

        elif "/chromosomeLength" in self.path:
            length= 0
            try:


                arguments = self.manage_arguments(self.path)
                specie = arguments["specie"]
                chromosome = arguments["chromo"]
                if "specie" in arguments and arguments['specie'] != "":
                    specie = arguments["specie"]
                    if "+" in specie:
                        specie = specie.replace("+", "_")
                conn = http.client.HTTPConnection("rest.ensembl.org")
                conn.request("GET", "/info/assembly/" + specie + "/" + chromosome + "?content-type=application/json")
                r1 = conn.getresponse()
                data1 = r1.read().decode("utf-8")
                response = json.loads(data1)
                length = response[length]

                if "json" in arguments:
                    json_response = True

                    if length != 0:
                        json_response = [specie, [chromosome, {"length": length}]]
                        contents = json.dumps(json_response)
                    else:
                        json_response = [specie, {chromosome: "not found in karyotype"}]
                        contents = json.dumps(json_response)
                else:
                    if length != 0:
                        contents = """
                                                            <html>
                                                            <body style= "background-color: pink;">
                                                            <ul>"""
                        contents = contents + "<li>" + "The length of the chromosome is: " + str(length) + "</li>"
                        contents = contents + """</ul>
                                                </body>
                                                </html>
                                            """
                    if length == 0:
                        contents = """
                                                                <html>
    
                                                                <body style= "background-color: pink;">
    
                                                                <ul>"""

                        contents = contents + "<li>" + " The length is: " + str(length)
                        contents = contents + " due to the chromosome introduced does not exist in the karyotype"
                        contents = contents + "of the specie " + specie + "</li>"
                        contents = contents + """</ul>
    
                                                    </body>
    
                                                    </html>
    
                                                """
            except KeyError:
                if "json" in self.path:
                    json_response = True
                    msg = "message from the server"
                    json_response = {msg: "you introduced a specie that is wrong or that is not in the data base"}
                    contents = json.dumps(json_response)
                else:
                    contents = """
                                                                 <html>
                                                                 <body>
                                                                 <ul>"""
                    contents = "you introduced a specie that is wrong or that is not in the data base"
                    contents = contents + """
                                                            </ul> 
                                                            </body>
                                                            </html>
                                                            """



        elif "/geneSeq" in self.path:
            arguments = self.manage_arguments(self.path)
            print("the arguments are;", arguments)
            try:
                gene = arguments["gene"]
                conn = http.client.HTTPConnection("rest.ensembl.org")
                # First I have to connect with the following url to access to the information of the gene introduced,
                # and get the identifier of that gene
                conn.request("GET", "/homology/symbol/human/" + gene + "?content-type=application/json")
                r1 = conn.getresponse()
                data1 = r1.read().decode("utf-8")
                response = json.loads(data1)
                identifier = response["data"][0]["id"]
                # The identifier will help us to connect to the following url for getting the sequence of dna
                conn.request("GET", "/sequence/id/" + identifier + "?content-type=application/json")
                r2 = conn.getresponse()
                data2 = r2.read().decode("utf-8")
                response_2 = json.loads(data2)
                seq_dna = response_2["seq"]

                if "json" in arguments:
                    json_response = True
                    json_response = {identifier: seq_dna}
                    contents = json.dumps(json_response)
                else:
                    contents = """
                                                        <html>
                                                        <body style= "background-color: pink;">
                                                        <ul>"""
                    contents = contents + "The sequence of the gene " + gene + " introduced is: " + seq_dna
                    contents = contents + """
                    </ul> 
                    </body>
                    </html>
                    """
            except KeyError:
                if "json" in self.path:
                    json_response = True
                    msg = "message from the server"
                    json_response = {msg: "you introduced an incorrect gene"}
                    contents = json.dumps(json_response)
                else:
                    contents = """
                                                                 <html>
                                                                 <body>
                                                                 <ul>"""
                    contents += "you introduced an incorrect gene"
                    contents = contents + """
                                                            </ul> 
                                                            </body>
                                                            </html>
                                                            """
        elif "/geneInfo" in self.path:
            try:
                arguments = self.manage_arguments(self.path)
                print("the arguments are", arguments)
                gene = arguments["gene"]
                conn = http.client.HTTPConnection("rest.ensembl.org")
                conn.request("GET", "/homology/symbol/human/" + gene + "?content-type=application/json")
                r1 = conn.getresponse()
                data1 = r1.read().decode("utf-8")
                response = json.loads(data1)
                print("the response is ", response)
                identifier = response["data"][0]["id"]
                print("the id is,", id)
                conn.request("GET", "/overlap/id/" + identifier + "?feature=gene;content-type=application/json")
                r2 = conn.getresponse()
                data2 = r2.read().decode("utf-8")
                response2 = json.loads(data2)
                print("the response 2 is ", response2)
                print(response2[0]["start"])
                start_point = response2[0]["start"]
                end_point = response2[0]["end"]
                print("the end is ", end_point, type(end_point))
                print("the start is ", start_point)
                length = end_point - start_point
                if "json" in arguments:
                    json_response = True
                    json_info = {"id": identifier, "start": start_point, "end": end_point, "length": length}
                    contents = json.dumps(json_info)
                else:
                    contents = """
                                                        <html>
                                                        <body style= "background-color: pink;">
                                                        <ul>"""
                    contents = contents + "The id of the gen " + "introduced is: " + str(identifier) + "\n"
                    contents = contents + ". The start point is: " + str(start_point) + "\n" + ". The ending point is: "
                    contents = contents + str(end_point) + "\n"
                    contents = contents + ". The length of the gene is: " + str(length) + "."
                    contents = contents + """
                        </ul>
                        </body>
                        </html>
                    """
            except KeyError:
                if "json" in self.path:
                    json_response = True
                    msg = "message from the server"
                    json_response = {msg: "you introduced an incorrect gene"}
                    contents = json.dumps(json_response)
                else:
                    contents = """
                                                                 <html>
                                                                 <body>
                                                                 <ul>"""
                    contents += "you introduced an incorrect gene"
                    contents = contents + """
                                                            </ul> 
                                                            </body>
                                                            </html>
                                                            """
        elif "/geneCal" in self.path:
            # For this elif I will need the document of Seq.py that it was created a few sessions ago
            try:
                arguments = self.manage_arguments(self.path)
                print("arguments are ", arguments)
                gene = arguments["gene"]
                print("the gene is", type(gene))
                conn = http.client.HTTPConnection("rest.ensembl.org")
                conn.request("GET", "/homology/symbol/human/" + gene + "?content-type=application/json")
                r1 = conn.getresponse()
                data1 = r1.read().decode("utf-8")
                print("data 1 is ", data1)
                response = json.loads(data1)
                print("response is ", response)
                identifier = response["data"][0]["id"]
                conn.request("GET", "/sequence/id/" + identifier + "?content-type=application/json")
                r2 = conn.getresponse()
                data2 = r2.read().decode("utf-8")
                response_2 = json.loads(data2)
                seq_dna = response_2["seq"]
                s1 = Seq(seq_dna)
                length = len(seq_dna)
                perc_a = s1.perc("A")
                perc_c = s1.perc("C")
                perc_t = s1.perc("T")
                perc_g = s1.perc("G")
                if "json" in arguments:
                    json_response = True
                    msga = "Percentage of A"
                    msgc = "Percentage of C"
                    msgt = "Percentage of T"
                    msgg = "Percentage of G"

                    json_info = {"length": length, msga: perc_a, msgc: perc_c, msgt: perc_t, msgg: perc_g}
                    contents = json.dumps(json_info)
                else:
                    contents = """
                                                          <html>
                                                          <body style= "background-color: pink;">
                                                          <ul>"""
                    contents = contents + "Total length of the gene introduced is: " + str(length)
                    contents = contents + ". The percentage of A is: " + "\n" + str(perc_a)
                    contents = contents + ". The percentage of T is: " + str(perc_t) + ". The percentage of G is: "
                    contents = contents + str(perc_g) + ". The percentage of C is: " + str(perc_c)
                    contents = contents + """
                    </ul> 
                    </body>
                    </html>
                    """
            except KeyError:
                if "json" in self.path:
                    json_response = True
                    msg = "message from the server"
                    json_response = {msg: "you introduced an incorrect gene"}
                    contents = json.dumps(json_response)
                else:
                    contents = """
                                                                                <html>
                                                                                <body>
                                                                                <ul>"""
                    contents += "you introduced an incorrect gene"
                    contents = contents + """
                                                                           </ul> 
                                                                           </body>

                                                                         </html>
                                                                           """
        elif "geneList" in self.path:
            try:
                arguments = self.manage_arguments(self.path)
                chromo = arguments["chromo"]
                start_point = arguments["start"]
                end_point = arguments["end"]
                conn = http.client.HTTPConnection("rest.ensembl.org")
                url0 = "/overlap/region/human/"
                url1 = "?content-type=application/json;feature=gene;feature=transcript;feature=cds;feature=exon"
                url2 = "?content-type=application/json;feature=gene;feature=transcript;feature=cds;feature=exon"
                conn.request("GET", url0 + str(chromo) + ":" + str(start_point) + "-" + str(end_point) + url1)
                print("Response", url0 + str(chromo) + ":" + str(start_point) + "-" + str(end_point) + url2)
                r1 = conn.getresponse()
                data1 = r1.read().decode("utf-8")
                response = json.loads(data1)
                # the following "if" I decided to do because when I introduced,
                # an end_point > 5000000 or an start_point > 5000000, I receive an error and the page fallen
                if int(end_point) > 5000000 or int(start_point) > 5000000:
                    with open("error.html", "r") as f:
                        contents = f.read()
                        status = 404
                print("Response", response)
                if "json" in arguments:
                    json_response = True
                    # The json_info_empty is created due to in the explanation of the "/geneList" appeared that if the
                    json_info_empty = []
                    for i in response:
                        if i["feature_type"] == "gene":
                            json_info = {"id": i["external_name"], "start": i["start"], "end": i["end"]}
                            json_info_empty.append(json_info)
                    print(json_info_empty)
                    # I try to write and end_point > start_point and when the json checkbox was desactivated was good,
                    # but when the json checkbox was activated the error html was send in json format
                    # I decided to do the following "if" in which I declare json_response = False for avoiding that fact
                    if int(end_point) < int(start_point):
                        with open("error.html", "r") as f:
                            contents = f.read()
                            status = 404
                            json_response = False
                            print("hello3")
                    # If len(json_info_empty) == 0 only can be if there is not information added to the json_info_empty,
                    # so if there is not information added to the json_info_empty, there are not genes in that interval
                    elif len(json_info_empty) == 0:
                        msg = {"message from the server": "You introduced an interval in which there are not genes"}
                        contents = json.dumps(msg)
                    elif len(json_info_empty) != 0:
                        contents = json.dumps(json_info_empty)

                else:
                    contents = """
                                                               <html>
                                                               <body style= "background-color: pink;">
                                                               <ul>"""

                    counter = 0
                    msg1 = "the name of the gene is: "
                    msg2 = "The start point is : "
                    msg3 = "The end point is :"
                    for i in response:
                        print(i)
                        if i["feature_type"] == "gene":
                            counter += 1
                            one = i["external_name"]
                            two = str(i["start"])
                            three = str(i["end"])
                            contents += "<li>" + (msg1 + one + ". " + msg2 + two + ". " + msg3 + three + "</li>")
                    # While counter be greater than zero means that we have found one or more genes
                    if counter == 0:
                        contents = contents + "sorry you introduced a limit in which there are not genes" + """
                        </ol> 
                        </body>
                        </html>
                        """
                    else:
                        contents = contents + """
                        </ol> 
                        </body>
                        </html>
                        """
            except KeyError:
                if "json" in self.path:
                    json_response = True
                    msg = "message from the server"
                    json_response = {msg: "you introduced an incorrect gene"}
                    contents = json.dumps(json_response)
                else:
                    contents = """
                                                                                <html>
                                                                                <body>
                                                                                <ul>"""
                    contents += "you introduced an incorrect gene"
                    contents = contents + """
                                                                           </ul> 
                                                                           </body>
                                                                           </html>
                                                                           """
            except TypeError:
                with open("error.html", "r") as f:
                    contents = f.read()
                    status = 404
                    json_response = False
            except ValueError:
                with open("error.html", "r") as f:
                    contents = f.read()
                    status = 404
                    json_response = False
        else:
            status = 404
            with open("error.html", "r") as f:
                contents = f.read()
                json_response = False
        self.send_response(status)  # -- Status line: OK!
        # Define the content-type header:
        if json_response:
            self.send_header("Content-Type", "application/json")
        else:
            self.send_header("Content-Type", "text/html")
        # Generating the response message
        self.send_header('Content-Length', len(str.encode(contents)))
        # The header is finished
        self.end_headers()
        # Send the response message
        self.wfile.write(str.encode(contents))
        return


Handler = TestHandler
socketserver.TCPServer.allow_reuse_address = True
# -- Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at PORT", PORT)
    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_close()
print("")
print("Server Stopped")
