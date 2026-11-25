def route_call(call_type):
    if call_type == "billing":
        return ["Knowledge_accuracy","resolution_quality"]
    elif call_type == "claims":
        return ["Knowledge_accuracy","resolution_quality"]
    elif   call_type == "complaint":
        return["tone_empathy","resolution_quality"]
    elif  call_type == "general_query":
        return["Knowledge_accuracy"]
    else:
        return["knowledge_accuracy"] #fallback

#---Step 2 Apply routing to dataset
#on the column predicted_call_type apply route_call and what route_call returns save it in new column evaluation_plan

def apply_routing(df):
    """ Adds evaluation_plan column to DataFrame"""

    df["evaluation_plan"] = df["predicted_call_type"].apply(route_call)
    return df