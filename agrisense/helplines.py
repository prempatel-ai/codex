# State-wise Official Agriculture Helpline Numbers
# Source: Official Government Data

STATE_HELPLINES = {
    "Andhra Pradesh": "1800-599-6222",
    "Arunachal Pradesh": "600-500-6066",
    "Assam": "1800-345-3611",
    "Bihar": "1800-3456-195",
    "Chhattisgarh": "0771-251-2100",
    "Delhi": "1800-180-1551",  # uses KCC
    "Goa": "0832-233-4251",
    "Gujarat": "1800-233-5500",
    "Haryana": "1800-180-1551",  # uses KCC
    "Himachal Pradesh": "1800-180-8090",
    "Jharkhand": "1800-212-1234",
    "Karnataka": "1800-425-3141",
    "Kerala": "1800-425-1661",
    "Madhya Pradesh": "0755-255-8823",
    "Maharashtra": "1800-120-4100",
    "Manipur": "1800-345-3821",
    "Meghalaya": "1800-345-3644",
    "Mizoram": "0389-234-0457",
    "Nagaland": "1800-345-3704",
    "Odisha": "155333",
    "Punjab": "1800-3000-1555",
    "Rajasthan": "1800-180-1551",  # KCC
    "Sikkim": "1800-345-3435",
    "Tamil Nadu": "1800-599-7636",
    "Telangana": "1800-425-3141",
    "Tripura": "0381-241-6079",
    "Uttar Pradesh": "1800-180-1551",  # KCC
    "Uttarakhand": "1800-180-1551",
    "West Bengal": "1800-345-0017"
}

def get_state_helpline(state_name):
    """
    Returns the helpline number for the given state.
    Returns None if state not found.
    """
    if not state_name:
        return None
    return STATE_HELPLINES.get(state_name, None)
