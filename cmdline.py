"""
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import datetime
import json

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

TYPE_CONVERTER = {
    int: int,
    str: str,
    float: float
}

class cmdlineTool:
    def __init__(self):
        self.curIndex = json.load(open("index.json"))
        self.isRunning = True

    def pushToMaster(self):
        json.dump(self.curIndex, open("index.json", "w"), indent=4)
        os.system(f"git commit -a -n -m \"CMDLINE Commit: {datetime.datetime.now()}\" && git push")
    
    def customInput(self, msg):
        return input(f"{msg}\n\n> ")
    
    def deleteItem(self):
        isItem = False
        while not isItem:
            clear()
            iid = self.customInput("What is the id of the item you would like to update?")
            if self.curIndex['items'].get(iid):
                isItem = True
            else:
                clear()
                if self.customInput("Item not found. Try again? (y/n)").lower() == "n":
                    isItem = True
        clear()
        if self.customInput(f"Are you sure you want to delete {iid}? (y/n)").lower() != "n":
            clear()
            if self.customInput(f"Are you really, really sure you want to delete it? (Cannot be undone) (y/n)").lower() != "n":
                clear()
                del self.curIndex['items'][iid]
                self.pushToMaster()    
    
    def updateItem(self):
        isEditing = True
        isItem = False
        tempItems = self.curIndex['items']
        while not isItem:
            clear()
            iid = self.customInput("What is the id of the item you would like to update?")
            if self.curIndex['items'].get(iid):
                isItem = True
                item = self.curIndex['items'][iid]
            else:
                if self.customInput("Item not found. Try again? (y/n)").lower() == "n":
                    isEditing = False
                    isItem = True
        while isEditing:
            clear()
            changableValues = [i for i in list(item.keys())]
            changableStr = ""
            for i in range(len(changableValues)-1):
                changableStr += f"{i+1}. {changableValues[i]}:type({type(item[changableValues[i]])}\n"
            changableStr += f"{len(changableValues)+1}. Change ID of Item\n"
            changableStr += f"{len(changableValues)+2}. Save And Exit\n"
            changableStr += f"{len(changableValues)+3}. Exit Without Saving"
            toEdit = int(self.customInput(f"What would you like to edit?\n\n{changableStr}"))
            if toEdit == len(changableValues)+1:
                clear()
                new = self.customInput("What is the name of the new id?").lower()
                if new.find(" ") != -1:
                    new = new.replace(" ", "-")
                if self.customInput(f"Change id from {iid} to {new}? (y/n)").lower() != "n":
                    tempItems[new] = self.curIndex['items'][iid]
                    del tempItems[iid]
                    iid = new
            elif toEdit == len(changableValues)+2:
                clear()
                tempItems[iid] = item
                self.curIndex['items'] = tempItems
                self.pushToMaster()
                isEditing = False
            elif toEdit == len(changableValues)+3:
                clear()
                isEditing = False
            else:
                clear()
                val = TYPE_CONVERTER[type(item[changableValues[toEdit-1]])](self.customInput(f"What would you like to change {changableValues[toEdit-1]} to?"))
                if self.customInput(f"Change value of {changableValues[toEdit-1]} to {val}? (y/n)").lower() != "n":
                    item[changableValues[toEdit-1]] = val
    
    def addItem(self):
        iid = self.customInput("Item ID")
        if not self.curIndex['items'].get(iid):
            clear()
            name = self.customInput("Item Name")
            clear()
            price = self.customInput("Item Price")
            clear()
            desc = self.customInput("Item Description")
            clear()
            longDesc = self.customInput("Item Long Description: ")
            clear()
            item = {
                "name": name,
                "price": float(price),
                "description": desc,
                "longDescription": longDesc
            }
            if self.customInput("Use img? (y/n)").lower() != "n":
                clear()
                item["img"] = self.customInput("Image URL")
            clear()
            if self.customInput("Use options? (y/n)").lower() != "n":
                x = ""
                item['options'] = []
                options = ['sizes', 'colors']
                for i in range(len(options)-1):
                    x += f"{i+1}. options[i]\n"
                # Fix this to actually loop later.
                match (self.customInput(f"What options would you like to add?\n\n{x}")):
                    case 1:
                        item["options"].append("sizes")
                    case 2:
                        item["options"].append("colors")
                clear()
                item["img"] = self.customInput("Image URL")
            clear()
            if self.customInput(f"Does this look okay to you? (y/n)\n\n{json.dumps(item, indent=4)}").lower() != "n":
                self.curIndex['items'][iid] = item
                self.pushToMaster()
        else:
            clear()
            self.customInput("Item already exists. Press any button to return to main...")

    def handleIn(self, curFunc):
        clear()
        match curFunc:
            case 1: # Add
                self.addItem()
            case 2: # Update
                self.updateItem()
            case 3: # Delete
                self.deleteItem()
            case 4: # Exit
                self.isRunning = False
            case default: # None
                self.customInput("Invalid input. Press any button to return to main...")
    
    def run(self):
        while self.isRunning:
            clear()
            curFunc = input("1. Add New Item\n2. Update Item\n3. Delete Item\n4. Exit\n\n> ")
            self.handleIn(int(curFunc))

cmdlineTool().run()