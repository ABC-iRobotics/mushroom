package hu.mushroom.datastore;

import org.springframework.stereotype.Component;

@Component
public class DatastoreMapper {
    
    public MushroomRow map(MushroomRowEntity entity) {
        var result = new MushroomRow();
        result.setCo2(entity.getCo2());
        result.setCompostTemp(entity.getCompostTemp());
        result.setDate(entity.getDate());
        result.setRh(entity.getRh());
        result.setRoomTemp(entity.getRoomTemp());
        return result;
    }

}
