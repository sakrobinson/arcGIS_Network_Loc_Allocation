# Uses Network Analyst to solve a simple location allocation problem for a fictional retail store chain. 
# In this problem, the goal is to identify the best locations for three new stores based on the proximity 
# to existing customers and the expected demand in each area.

# First, we need to create a network dataset from our road network data using the "CreateNetworkDataset" tool.
import arcpy

# Set the workspace and output folder
arcpy.env.workspace = r"C:\data"
output_folder = r"C:\output"

# Create a network dataset from the road network data
in_network_dataset = r"C:\data\road_network.nd"
out_network_dataset = output_folder + "\store_allocation_network.nd"
arcpy.na.CreateNetworkDataset(in_network_dataset, out_network_dataset)

# Next, we need to add our existing customers to the network dataset using the "AddLocations" tool, 
# and set their demand levels based on their purchase history.
# Add existing customers as facilities
in_facilities = output_folder + "\existing_customers.shp"
arcpy.na.AddLocations(out_network_dataset, "Facilities", in_facilities)

# Set demand levels for each facility based on purchase history
field_mappings = arcpy.na.NAClassFieldMappings(out_network_dataset, "Facilities")
field_mappings["Demand"].mappedFieldName = "PurchaseHistory"
arcpy.na.UpdateFieldMappings(out_network_dataset, "Facilities", field_mappings)

# Next, we need to define the potential new store locations using a point feature class.
# Define potential new store locations as demand points
in_demand_points = output_folder + "\potential_store_locations.shp"
arcpy.na.AddLocations(out_network_dataset, "DemandPoints", in_demand_points)

# Now we can solve the location allocation problem using the "Solve" tool, which will identify 
# the best locations for three new stores based on the proximity to existing customers and the expected demand in each area.
# Solve the location allocation problem
in_analysis_layer = arcpy.na.MakeLocationAllocationLayer(out_network_dataset, "Store Allocation", "DemandPoints", "Facilities", "Demand", 3)
arcpy.na.Solve(in_analysis_layer)

#Finally, we can export the results to a feature class and visualize them as desired
# Export the results to a feature class
out_allocation_results = output_folder + "\store_allocation_results.shp"
arcpy.management.CopyFeatures(in_analysis_layer.solverProperties.outputPaths[1], out_allocation_results)

# Visualize the results on a map (optional)
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)[0]
layer = arcpy.mapping.Layer(out_allocation_results)
arcpy.mapping.AddLayer(df, layer)
arcpy.RefreshActiveView()
