# Symptomic
## a tracker of tweets containing symptoms of pathogens

In this project, we try to find tweets of people showing symptoms (e.g. coughing, sneezing, fever). Goal is to track pathogens on twitter and see if we can predict (in a machine learning way) the development of diseases.

## Files

### settings.cfg
This file contains the configuration of the tracker. It consists of three sections: [credentials], [track], and [output]
#### [credentials]
This section holds the access key and secret, and the consumer key and secret for the twitter API. Please register the project at twitter and generate the keys.

#### [track]
This section holds the distinct terms to track. This is done in an AND/OR fashion: all terms in one line have to appear, one of the lines has to appear. For example:</br>
```
    [track]
    tags = 
      I cough 
      I coughing
      I fever
      I sneeze
      I sneezing
```
   
is interpreted as:
```
    (I AND cough) OR (I AND coughing) OR (I and fever) OR (I and sneeze) OR (I and sneezing)
```

#### [output]
the output of the listener will be written to output/<filename>
  
  
