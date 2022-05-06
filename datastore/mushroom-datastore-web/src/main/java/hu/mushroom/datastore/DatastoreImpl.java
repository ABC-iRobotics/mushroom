package hu.mushroom.datastore;

import java.util.Set;

import org.springframework.web.bind.annotation.RestController;

@RestController
public class DatastoreImpl implements DatastoreApi {
    
    private final DatastoreService service;
    
    public DatastoreImpl(DatastoreService service) {
        this.service = service;
    }

    @Override
    public void storeData(String filename) {
        service.storeData(filename);
    }

    @Override
    public Set<MushroomRow> getAllData() {
        return service.getAll();
    }

}
