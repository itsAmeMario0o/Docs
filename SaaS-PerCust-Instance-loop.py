import sys
from  acitoolkit.acitoolkit import *

# Creating an empty tenant list.
tenant_list =[]

# Let's create 10 tenants, with all their EPGs, VRFs, BDs
for i in range(1, 11):

    #Tenant Creation - We will create a Tenant on a per customer basis. This is one way leverage Tenants.
    # my str(i) is used to as a identifier and a delimiter
    tenant = Tenant('Customer'+ str(i))
    
    #VRF creation, isolate each customer IP space
    context= Context('Customer' + str(i) + '-Router', tenant)
    
    #BridgeDomain, under the Context/Tenant created above
    bd-FE = BridgeDomain('Front-End'+str(i), tenant)
    bd-FE.add_context(context)

    bd-BE = BridgeDomain('Back-End' + str(i), tenant)
    bd-BE.add_context(context)

    #Creation of the AppProfile - Will you take the Red or the Blue pill? too many pills here :)
    app = AppProfile('APP' + str(i), tenant)
    
    #Create the EPG Front-End and attach it to the BD-FE
    FE = EPG('Front-End' + str(i), app )
    FE.add_bd(bd-FE)
    
    #Create the EPG Back-End and attach it to the BD1
    blue = EPG('Back-End' + str(i), app )
    blue.add_bd(bd-BE)

    # Adding the newly created the Tenant to our list. Next please...
    tenant_list.append(tenant)


# Getting credentials from the command line.
description = 'VoD application'
creds = Credentials('apic', description)
creds.add_argument('--delete', action='store_true',
               help='Delete the configuration from the APIC')
               
args = creds.get()

# Delete the configuration if desired
if args.delete:
            tenant.mark_as_deleted()

# Login to APIC
session = Session(args.url, args.login, args.password)
session.login()

# Now we'll actually push what we created. All the tenants in our list.
for tenant in tenant_list:
    
    if args.delete:
        tenant.mark_as_deleted()
        
    resp = tenant.push_to_apic(session)
    if resp.ok:
        print 'Success'

    # Print what was sent
    print 'Pushed the following JSON to the APIC'
    print 'URL:', tenant.get_url()
    print 'JSON:', tenant.get_json()
    print
