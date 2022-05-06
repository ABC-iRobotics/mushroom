package hu.mushroom.datastore;

import java.util.Set;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;

@RequestMapping("/api/Datastore")
public interface DatastoreApi {

    @GetMapping(value = "/StoreData/{filename}")
    void storeData(@PathVariable(value = "filename") String filename);
    
    @GetMapping(value = "/StoreData", produces = MediaType.APPLICATION_JSON_VALUE)
    Set<MushroomRow> getAllData();
    
}
