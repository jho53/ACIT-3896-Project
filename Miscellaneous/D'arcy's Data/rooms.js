const fs = require('fs');

class Rooms
{
    constructor(dir)
    {
        const buffer = fs.readFileSync(`${dir}/rooms.json`);

        this.database = JSON.parse(buffer.toString());
    }

    getRoom(roomId)
    {
        const roomInfo = this.database.rooms[roomId];

        if(!(roomInfo))
        {
            throw new Error("room: '" + roomId + "' does not exist");
        }

        return roomInfo;
    }
}

module.exports =
    {
        Rooms: Rooms
    }
