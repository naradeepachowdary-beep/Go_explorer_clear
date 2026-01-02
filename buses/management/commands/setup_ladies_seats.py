from django.core.management.base import BaseCommand
from buses.models import Bus, SeatLayout


class Command(BaseCommand):
    help = 'Setup ladies seats for buses'

    def handle(self, *args, **options):
        # Get all buses
        buses = Bus.objects.all()
        
        for bus in buses:
            # Clear existing seats
            SeatLayout.objects.filter(bus=bus).delete()
            
            # Create seat layout based on bus type
            if bus.bus_type in ['seater', 'ac_seater']:
                # 2x10 layout for seater buses
                seats_created = 0
                for row in range(1, 11):
                    for col in range(1, 3):
                        seat_number = f"{row}{chr(64+col)}"  # 1A, 1B, 2A, 2B, etc.
                        
                        # Mark alternate rows as ladies seats (starting from row 2)
                        reserved_for = 'ladies' if row % 2 == 0 else 'general'
                        
                        SeatLayout.objects.create(
                            bus=bus,
                            seat_number=seat_number,
                            seat_type='seater',
                            row=row,
                            column=col,
                            deck=1,
                            reserved_for=reserved_for,
                        )
                        seats_created += 1
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created {seats_created} seats for {bus.bus_number} (Seater)'
                    )
                )
            
            elif bus.bus_type in ['sleeper', 'ac_sleeper']:
                # 2x12 layout with lower and upper berths
                seats_created = 0
                for deck in [1, 2]:
                    deck_name = 'Lower' if deck == 1 else 'Upper'
                    for row in range(1, 7):
                        for col in range(1, 3):
                            seat_number = f"{row}{chr(64+col)}{deck_name[0]}"  # 1AL, 1AU, 2AL, 2AU, etc.
                            seat_type = 'sleeper_lower' if deck == 1 else 'sleeper_upper'
                            
                            # Mark women section (rows 1-2) as ladies seats
                            reserved_for = 'ladies' if row <= 2 else 'general'
                            
                            SeatLayout.objects.create(
                                bus=bus,
                                seat_number=seat_number,
                                seat_type=seat_type,
                                row=row,
                                column=col,
                                deck=deck,
                                reserved_for=reserved_for,
                            )
                            seats_created += 1
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created {seats_created} seats for {bus.bus_number} (Sleeper)'
                    )
                )
            
            else:
                # Default layout for other bus types
                total_seats = bus.total_seats
                seats_created = 0
                seat_num = 0
                
                for row in range(1, (total_seats // 2) + 1):
                    for col in range(1, 3):
                        seat_num += 1
                        if seat_num > total_seats:
                            break
                        
                        reserved_for = 'ladies' if row % 2 == 0 else 'general'
                        
                        SeatLayout.objects.create(
                            bus=bus,
                            seat_number=str(seat_num),
                            seat_type='seater',
                            row=row,
                            column=col,
                            deck=1,
                            reserved_for=reserved_for,
                        )
                        seats_created += 1
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created {seats_created} seats for {bus.bus_number} ({bus.get_bus_type_display()})'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                'Ladies seat setup complete! Alternate rows/sections are reserved for ladies.'
            )
        )
