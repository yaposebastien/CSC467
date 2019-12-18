import geni.portal as portal
import geni.rspec.pg as pg
import geni.rspec.igext as IG

pc = portal.Context()
request = pc.makeRequestRSpec()

tourDescription = "A compute node with Docker installed on Ubuntu 18.04" 
tour = IG.Tour()
tour.Description(IG.Tour.TEXT,tourDescription)
request.addTour(tour)

node = request.RawPC("head")
node.routable_control_ip = "true" 
node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD"
node.addService(pg.Execute(shell="sh", command="sudo bash /local/repository/install_docker.sh")) 
pc.printRequestRSpec(request)
