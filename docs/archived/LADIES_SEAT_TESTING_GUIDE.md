# Ladies Seat Reservation - Quick Testing Guide

## Prerequisites
- Server running: `python manage.py runserver`
- At least one bus with routes configured
- Test user accounts (male and female) created

## Quick Test Workflow

### 1. Create Test User (if needed)
```bash
python manage.py createsuperuser
# OR use existing test accounts
```

### 2. Start Development Server
```bash
python manage.py runserver
```

### 3. Access Bus Listing
```
URL: http://localhost:8000/buses/
```

### 4. Select a Bus
Click on any bus to view its details:
```
URL: http://localhost:8000/buses/<bus_id>/?route_id=<route_id>&travel_date=<YYYY-MM-DD>
```

### 5. Expected Seat Layout Display

#### Visual Elements
- ✅ Seat map displays all seats in rows
- ✅ Green seats = Available general seats
- ✅ Pink seats = Ladies-only seats
- ✅ Red seats = Already booked
- ✅ Legend shows color meanings at top

#### Example Seat Numbers
- Seater buses: 1A, 1B, 2A, 2B, ... (row + column letter)
- Sleeper buses: 1AL, 1AU, 2AL, 2AU, ... (row + column + deck)

---

## Test Cases

### Test Case 1: Female Passenger Books Ladies Seat
**Expected**: ✅ Success

1. Login as female user
2. Fill passenger details:
   - Name: Female Test
   - Age: 25
   - **Gender: Female**
3. Click on pink (ladies) seat
4. Verify: Blue highlight appears on selected seat
5. Check "Selected Seats" shows the seat number
6. Click "Book Now"
7. **Result**: Booking confirmation shown

**Terminal Output**:
```
✅ BusBookingSeat created for female passenger on ladies seat
✅ Booking status: confirmed
```

---

### Test Case 2: Male Passenger Tries Ladies Seat
**Expected**: ❌ Error Message

1. Login as male user
2. Fill passenger details:
   - Name: Male Test
   - Age: 30
   - **Gender: Male**
3. Click on pink (ladies) seat
4. Verify: Blue highlight appears on selected seat
5. Check "Selected Seats" shows the seat number
6. Notice: Yellow warning box appears:
   ```
   ⚠️ Male passengers cannot book ladies seats. 
   Please select different seats.
   ```
7. Click "Book Now" button
8. **Result**: Button disabled (grayed out)

**What User Must Do**:
- Click selected ladies seat again to deselect (blue highlight removed)
- Select a green (general) seat instead
- Warning disappears
- Click "Book Now" to proceed

---

### Test Case 3: Mixed Seat Selection (Male + Ladies)
**Expected**: ❌ Error (cannot book)

1. Login as male user
2. Fill passenger details (Male)
3. Click on green (general) seat = Blue highlight
4. Click on pink (ladies) seat = Blue highlight
5. Notice: Warning appears immediately
6. "Book Now" button disabled
7. **Result**: Cannot proceed without removing ladies seat

---

### Test Case 4: Multiple Seats Available
**Expected**: ✅ All available seats clickable

1. View seat layout
2. Count available green seats (not gray/red)
3. Click several green seats
4. Verify: Each click highlights a new seat (blue)
5. "Selected Seats" updates: "3 seat(s): 1A, 1B, 2A"
6. Price updates:
   ```
   Base Fare (per seat): ₹1000 × 3 seats = ₹3000
   Convenience Fee (2%): ₹60
   GST (5%): ₹153
   Total: ₹3213
   ```
7. "Book Now" enabled
8. Submit booking

---

### Test Case 5: Booked Seats Not Selectable
**Expected**: ❌ Grayed out (no click)

1. View seat layout
2. Identify red seats (booked)
3. Try clicking red seat
4. Verify: No blue highlight appears
5. "Book Now" button remains disabled
6. **Result**: Booked seats cannot be selected

---

## Validation Checks in Browser

### Console Validation (F12 → Console)
```javascript
// Should log selected seats
console.log(document.querySelectorAll('.seat-checkbox:checked').length);
// Example output: 2

// Check gender value
console.log(document.getElementById('passenger_gender').value);
// Example output: "F" or "M"
```

### Form Validation
- Passenger name: Required (cannot be empty)
- Age: Required (number only, >= 1)
- Gender: Required (select from dropdown)
- Travel date: Required (cannot be in past)
- Boarding point: Required
- Dropping point: Required
- **At least 1 seat selected**: Required

---

## Backend Validation (Server Logs)

### Successful Booking
```log
[INFO] buses.views: Female passenger booking ladies seat
[INFO] buses.views: Seat validation passed for 1 seat
[INFO] buses.views: BusBookingSeat created: Seat 2B
[INFO] buses.views: Booking confirmed: UUID-XXXX
```

### Failed Booking
```log
[ERROR] buses.views: Gender mismatch detected
[ERROR] buses.views: Seat 2B reserved_for='ladies' but passenger_gender='M'
[ERROR] Return error: Male passengers cannot book ladies seats
```

---

## Database Verification

### Check Seats in Django Shell
```bash
python manage.py shell
```

```python
from buses.models import Bus, SeatLayout

# Get a bus
bus = Bus.objects.first()

# Check seat distribution
ladies_seats = bus.seat_layout.filter(reserved_for='ladies').count()
general_seats = bus.seat_layout.filter(reserved_for='general').count()
disabled_seats = bus.seat_layout.filter(reserved_for='disabled').count()

print(f"Ladies: {ladies_seats}, General: {general_seats}, Disabled: {disabled_seats}")
# Example output: Ladies: 20, General: 28, Disabled: 0

# Check a specific seat
seat = SeatLayout.objects.get(bus=bus, seat_number='2A')
print(seat.reserved_for)  # Should print 'ladies' or 'general'
print(seat.can_be_booked_by('F'))  # True if female can book
print(seat.can_be_booked_by('M'))  # False if ladies seat and male passenger
```

---

## Troubleshooting

### Issue 1: Seats Not Showing
**Check**:
1. Is `{% if seats %}` block rendering?
2. Are seats in database? Run:
   ```bash
   python manage.py shell
   from buses.models import Bus
   bus = Bus.objects.first()
   print(bus.seat_layout.count())  # Should be > 0
   ```

### Issue 2: Ladies Seat Warning Not Showing
**Check**:
1. Is JavaScript loading? (Check F12 → Sources)
2. Is `validateLadiesSeats()` function defined?
3. Is `passenger_gender` value being read correctly?

### Issue 3: Booking Button Always Disabled
**Check**:
1. Are seats selected? (Blue highlight visible?)
2. Check browser console for JavaScript errors
3. Verify `bookNowBtn.disabled` state

### Issue 4: Can Book Ladies Seat as Male
**Check**:
1. Verify `can_be_booked_by()` method in model
2. Check `book_bus()` view has validation code
3. Test with: `python manage.py shell` → `seat.can_be_booked_by('M')`

---

## Performance Testing

### Load Test: Multiple Seat Selections
```
1. Select 10 seats one by one
2. Measure response time (should be instant)
3. Verify price updates immediately
4. Check network tab (should be 0 requests)
```

### Database Query Test
```python
from django.db import connection
from django.test.utils import override_settings

@override_settings(DEBUG=True)
def test():
    from buses.views import bus_detail
    # View should use < 5 database queries
    print(len(connection.queries))
```

---

## Mobile Testing

### Responsive Layout
1. Open DevTools (F12)
2. Toggle Device Toolbar (Ctrl+Shift+M)
3. Test on iPhone 12, iPad, Android devices
4. Verify:
   - Seats are clickable (not too small)
   - Layout doesn't overflow
   - Form is readable
   - Price updates show

### Touch Interactions
1. Tap seats (should highlight blue)
2. Tap again to deselect (blue removed)
3. Verify legend still visible
4. Book button should be reachable without scrolling

---

## Success Criteria

| Test | Expected | Status |
|------|----------|--------|
| Female books ladies seat | ✅ Success | [ ] |
| Male books ladies seat | ❌ Error | [ ] |
| Female books general seat | ✅ Success | [ ] |
| Male books general seat | ✅ Success | [ ] |
| Booked seats blocked | ❌ Cannot select | [ ] |
| Price calculates correctly | ✅ Accurate | [ ] |
| Seat layout displays | ✅ Visible | [ ] |
| Gender validation works | ✅ Working | [ ] |
| Mobile responsive | ✅ Good | [ ] |

---

## Next Steps After Testing

1. **Pass All Tests** → Mark as ready for production
2. **Log Issues Found** → Create GitHub issues for fixes
3. **Get User Feedback** → Ask real users to test
4. **Performance Tuning** → Optimize queries if needed
5. **Security Audit** → Check for CSRF, XSS vulnerabilities
6. **Deploy to Production** → After approval

---

**Last Updated**: 2024-01-XX  
**Tested By**: [Your Name]  
**Status**: Ready for QA
