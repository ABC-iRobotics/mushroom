package hu.mushroom.datastore;

import java.util.Set;
import java.util.UUID;
import java.util.stream.Collectors;

import javax.transaction.Transactional;

import org.springframework.http.MediaType;
import org.springframework.http.RequestEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
@Transactional
public class DatastoreService {

    private final MushroomRowRepository repository;
    private final DatastoreMapper mapper;
    private final RestTemplate restTemplate;
    private final MushroomDatastoreConfigurationProperties config;

    public DatastoreService(MushroomRowRepository repository, DatastoreMapper mapper, MushroomDatastoreConfigurationProperties config) {
        this.repository = repository;
        this.mapper = mapper;
        this.restTemplate = new RestTemplate();
        this.config = config;
    }

    public void storeData(String filename) {
        MushroomDocument document = getAll(filename);
        for(var row : document.getRows()) {
            storeSingleRow(row, filename);
        }
    }

    private void storeSingleRow(MushroomRow row, String filename) {
        MushroomRowEntity entity = new MushroomRowEntity();
        entity.setId(UUID.randomUUID().toString());
        entity.setDocumentName(filename);
        entity.setCo2(row.getCo2());
        entity.setCompostTemp(row.getCompostTemp());
        entity.setDate(row.getDate());
        entity.setRh(row.getRh());
        entity.setRoomTemp(row.getRoomTemp());
        
        repository.save(entity);
    }

    public Set<MushroomRow> getAll() {
        return repository.findAll().stream().map(mapper::map).collect(Collectors.toSet());
    }

    private MushroomDocument getAll(String filename) {
        return restTemplate.exchange(RequestEntity
                .get(config.getXpsParserUrl() + filename)
                .accept(MediaType.APPLICATION_JSON)
                .build(), MushroomDocument.class).getBody();
    }
}
