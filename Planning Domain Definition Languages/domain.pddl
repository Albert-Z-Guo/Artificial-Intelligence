(define (domain sokorobotto)
    (:requirements :typing)
    (:types shipment order location moving_object saleitem - object
            robot pallette - moving_object)
    (:predicates
        (includes ?shipment - shipment ?saleitem - saleitem)
        (unstarted ?shipment - shipment)
        (ships ?shipment - shipment ?order - order)
        (orders ?order - order ?saleitem - saleitem)

        (packing-location ?pack - location)
        (available ?pack - location)

        (free ?robot - robot)
        (contains ?pallette - pallette ?saleitem - saleitem)

        (connected ?loc1 ?loc2 - location)
        (no-robot ?loc - location)
        (no-pallette ?pack - location)

        (at ?moving_object - moving_object ?loc - location)
        (pickedup ?robot - robot ?pallette - pallette)

        (designated-packing-location ?shipment - shipment ?loc - location)
    )


    (:action free_move
        :parameters (?robot - robot ?loc1 - location ?loc2 - location)
        :precondition (and (free ?robot) (connected ?loc1 ?loc2) (at ?robot ?loc1) (no-robot ?loc2))
        :effect (and (not (at ?robot ?loc1)) (no-robot ?loc1)
                    (at ?robot ?loc2) (not (no-robot ?loc2))
        )
	  )


    (:action pick_up_pallette
        :parameters (?robot - robot ?loc - location ?pallette - pallette )
        :precondition (and (free ?robot) (at ?robot ?loc) (at ?pallette ?loc))
        :effect (and (not (free ?robot)) (pickedup ?robot ?pallette))
    )


    (:action carry_pallette
        :parameters (?robot - robot ?pallette - pallette ?loc1 - location ?loc2 - location)
        :precondition (and (not (free ?robot)) (pickedup ?robot ?pallette)
                          (at ?robot ?loc1) (connected ?loc1 ?loc2) (no-robot ?loc2) (no-pallette ?loc2)
        )
        :effect (and (not (at ?robot ?loc1)) (no-robot ?loc1)
                      (at ?robot ?loc2) (not (no-robot ?loc2))

                      (not (at ?pallette ?loc1)) (no-pallette ?loc1)
                      (at ?pallette ?loc2) (not (no-pallette ?loc2))
        )
  	)


  	(:action drop_pallete
          :parameters (?robot - robot ?loc - location ?pallette - pallette)
          :precondition (and (not (free ?robot)) (at ?robot ?loc)
                              (pickedup ?robot ?pallette)

                              (not (packing-location ?loc)) ; do not drop the pallete at a packing location
          )
          :effect (and
                      (at ?pallette ?loc) (not (no-pallette ?loc))
                      (not (pickedup ?robot ?pallette))
                      (free ?robot)
          )
  	)


    (:action start_shipment_at_a_packing_location
        :parameters (?shipment - shipment ?pack - location)
        :precondition (and (unstarted ?shipment)
                            (available ?pack) ; designate a shipment only if there's an available packing location
        )
        :effect (and (not (unstarted ?shipment))
                    (designated-packing-location ?shipment ?pack) ; designate a packing location
                    (not (available ?pack)) ; mark the designated packing location unavailable
        )
    )
    
    
    (:action load_shipment
        :parameters (?robot - robot ?pallette - pallette ?pack - location ?saleitem - saleitem ?order - order ?shipment - shipment)
        :precondition (and (not (free ?robot)) (at ?robot ?pack)
                            (packing-location ?pack) ; include shipment at packing-location if the rest conditions are met
                            (at ?pallette ?pack)

                            (pickedup ?robot ?pallette)
                            (contains ?pallette ?saleitem)

                            (not (unstarted ?shipment)) ; the unstarted shipment is associated with an order and a saleitem
                            (ships ?shipment ?order) (orders ?order ?saleitem)

                            (designated-packing-location ?shipment ?pack) ; the started shipment is associated with a packing location
        )
        :effect (and (not (contains ?pallette ?saleitem))
                    (includes ?shipment ?saleitem)
        )
    )
    
    
    (:action check_packing_location_availability
        :parameters (?pack - location ?shipment - shipment ?saleitem - saleitem)
        :precondition (and (not (available ?pack))
                            (designated-packing-location ?shipment ?pack)
                            (includes ?shipment ?saleitem)
        )
        :effect (available ?pack)
    )
)
