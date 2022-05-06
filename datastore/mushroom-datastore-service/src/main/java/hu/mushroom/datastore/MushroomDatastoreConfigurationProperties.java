package hu.mushroom.datastore;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

import lombok.Data;

@ConfigurationProperties(prefix = "biofungi")
@Component
@Data
public class MushroomDatastoreConfigurationProperties {
    
    private String xpsParserUrl;

}
