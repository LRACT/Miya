async def get_team(user_id, app): 
    t_members = app.team.members
    owner = False
    for t in t_members:
        if t.id == user_id:
            owner = True
    
    return owner