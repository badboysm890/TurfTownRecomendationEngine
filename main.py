from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
# import the library file for jsonifying the data
from fastapi.responses import JSONResponse
import mongo_lib
import geo
import datetime
app = FastAPI()

# Setup Middleware for CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/getPredictions/{email_id}")
async def root(email_id: str):
    userData = mongo_lib.findUserDetails("email", email_id, "users")
    GameData = mongo_lib.getGamesByDays(3)
    predictions = []
    for i in GameData:
        dataPoints = {
            "dateScore" : 0,
            "filled" : 0,
            "sports" : 0,
            "venues" : 0,
            "followers" : 0,    
            "location" : 0,
            "invite" : 0,
        }
        tdy = datetime.datetime.now()
        diff = i["booking_date"] - tdy
        if diff.days == 0:
            dataPoints["dateScore"] = 25
        elif diff.days == 1:
            dataPoints["dateScore"] = 25/2
        elif diff.days == 2:
            dataPoints["dateScore"] = 25/3
        offline = 0
        try:
         offline = len(i["offline_users"])
        except:
            print("no offline users")

        filled = ((len(i["users"])+offline)/i["limit"])*100
        FilledData = 0.1 * filled
        dataPoints["filled"] = FilledData
        userFavSport = userData["user_profile"]["fav_sports"]
        sports = i["sport_name"]
        if sports in userFavSport:
            dataPoints["sports"] = 50*1
        # ----------------------------------- venues data -----------------------------------
        userFavVenues = userData["user_profile"]["fav_venues"]
        # print(userFavVenues)
        # it takes too much time
        # ----------------------------------- venues data -----------------------------------
        userFollowers = userData["user_profile"]["followers"]
        userFollowing = userData["user_profile"]["following"]
        creator = ""
        try:
         creator = i["users"][0]
        except:
          pass

        if creator in userFollowers:
            dataPoints["followers"] = 5*1
        elif  creator in userFollowing:
            dataPoints["followers"] = 5*1

        location = userData["user_profile"]["location"]
        for j in  i["bookings"]:
           if geo.distance(float(location["lat"]), float(location["lng"]),float(j["venue_data"]["venue"]["latLong"][0]), float(j["venue_data"]["venue"]["latLong"][1])) < 5:
              dataPoints["location"] = 5*1
           elif geo.distance(float(location["lat"]), float(location["lng"]),float(j["venue_data"]["venue"]["latLong"][0]), float(j["venue_data"]["venue"]["latLong"][1])) < 10:
              dataPoints["location"] = 5*0.5
           else:
              dataPoints["location"] = 5*0
           break

        total_sum = sum(dataPoints.values())
        predictions.append({"game_id": str(i["_id"]), "prediction": total_sum})
        sortedPredictions = sorted(predictions, key=lambda k: k['prediction'], reverse=True)
        Predictions = sortedPredictions[:20]
    return JSONResponse(content={"message": Predictions}, status_code=200)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)   