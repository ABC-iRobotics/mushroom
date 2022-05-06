package hu.mushroom.datastore;

import java.math.BigDecimal;
import java.time.ZonedDateTime;

import com.fasterxml.jackson.annotation.JsonFormat;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class MushroomRow {

    private BigDecimal compostTemp;
    private BigDecimal roomTemp;
    private BigDecimal co2;
    private BigDecimal rh;

    @JsonFormat(pattern = "EEE, dd MMM yyyy HH:mm:ss z")
    private ZonedDateTime date;

}
