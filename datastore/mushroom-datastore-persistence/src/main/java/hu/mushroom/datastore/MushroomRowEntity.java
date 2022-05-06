package hu.mushroom.datastore;

import java.math.BigDecimal;
import java.time.ZonedDateTime;

import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Entity
@Table(name = "mushroom_rows")
public class MushroomRowEntity {
    
    @Id
    private String id;
    private String documentName;
    private BigDecimal compostTemp;
    private BigDecimal roomTemp;
    private BigDecimal co2;
    private BigDecimal rh;
    private ZonedDateTime date;

}
