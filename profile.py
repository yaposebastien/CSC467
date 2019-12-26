# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
import geni.rspec.igext as IG

# Create a portal context.
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

pc.defineParameter("workerCount", "Number of DataNodes",
                   portal.ParameterType.INTEGER, 4)

#
# Get any input parameter values that will override our defaults.
#
params = pc.bindParameters()
pc.verifyParameters()

tourDescription = \
"""
This profile provides the template for a Hadoop cluster with 1 name node and customizable number of data nodes.
"""

tourInstructions = \
"""
After your instance boots (approx. 10-15 minutes), you can begin the setup process using 
[Ambari Server WebUI](http://{host-namenode}:8080/) with the default admin/admin as username and password. 
"""

#
# Setup the Tour info with the above description and instructions.
#  
tour = IG.Tour()
tour.Description(IG.Tour.TEXT,tourDescription)
tour.Instructions(IG.Tour.MARKDOWN, tourInstructions)

request.addTour(tour)

prefixForIP = "192.168.1."

link = request.LAN("lan")

for i in range(params.workerCount + 1):
  if i == 0:
    node = request.XenVM("namenode")
  else:
    node = request.XenVM("datanode-" + str(i))
  node.cores = 4
  node.ram = 8192
  node.routable_control_ip = "true"
  node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:CENTOS7-64-STD"
  bs = node.Blockstore("bs" + str(i), "/hadoop")
  bs.size = "100GB"
   
  if i == 0:
    bs_landing = node.Blockstore("bs_landing", "/landing")
    bs_landing.size = "300GB"
    
  iface = node.addInterface("if" + str(i-3))
  iface.component_id = "eth1"
  iface.addAddress(pg.IPv4Address(prefixForIP + str(i + 1), "255.255.255.0"))
  link.addInterface(iface)
  
  node.addService(pg.Execute(shell="sh", command="sudo bash /local/repository/environment_prep.sh"))
  node.addService(pg.Execute(shell="sh", command="sudo bash /local/repository/setup_jupyter.sh"))
    
  if i == 0:
    node.addService(pg.Execute(shell="sh", command="sudo yum install -y ambari-server"))
    node.addService(pg.Execute(shell="sh", command="sudo ambari-server setup -s"))
    node.addService(pg.Execute(shell="sh", command="sudo yum -y install mysql-connector-java*"))
    node.addService(pg.Execute(shell="sh", command="sudo ln -s /usr/share/java/mysql-connector-java.jar /var/lib/ambari-server/resources/mysql-connector-java.jar"))
    node.addService(pg.Execute(shell="sh", command="sudo ambari-server start"))
    
  node.addService(pg.Execute(shell="sh", command="sudo yum install -y ambari-agent"))
  node.addService(pg.Execute(shell="sh", command="sudo sed -i 's/localhost/192.168.1.1/g' /etc/ambari-agent/conf/ambari-agent.ini"))
  node.addService(pg.Execute(shell="sh", command="sudo ambari-agent start"))
    
# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
