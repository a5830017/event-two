from django.test import TestCase
from event.models import Event, Person


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_displays_event_name(self):
        Event.objects.create(event_name='Event 1', event_detail='Detail 1',
            event_numset=2, event_location='Location 1', pcount=0,)

        response = self.client.get('/')

        self.assertIn('Event 1', response.content.decode())

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Event.objects.count(), 0)


class CreateEventPageTest(TestCase):

    def test_uses_template(self):
        response = self.client.get('/new_event')
        self.assertTemplateUsed(response, 'create_event.html')

    def test_can_save_a_POST_request(self):
        self.client.post('/new_event', data={'name': 'event name' , 'detail': 'event detail', 'numset': 10, 'location': 'event location'})

        self.assertEqual(Event.objects.count(), 1)
        new_event = Event.objects.first()
        self.assertEqual(new_event.event_name, 'event name')
        self.assertEqual(new_event.event_detail, 'event detail')
        self.assertEqual(new_event.event_numset, 10)
        self.assertEqual(new_event.event_location, 'event location')
        self.assertEqual(new_event.pcount, 0)

    def test_redirects_after_POST(self):
        response = self.client.post('/new_event', data={'name': 'event name' , 'detail': 'event detail', 'numset': 10, 'location': 'event location'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_only_saves_items_when_necessary(self):
        self.client.get('/new_event')
        self.assertEqual(Event.objects.count(), 0)
        


class DetailEventPageTest(TestCase):

    def test_uses_template(self):
        Event.objects.create(event_name='Event 1', event_detail='Detail 1',
            event_numset=2, event_location='Location 1', pcount=0,)

        response = self.client.get('/1/')
        self.assertTemplateUsed(response, 'detail.html')

    def test_displays_person_list_name(self):
        event = Event.objects.create(event_name='Event 1', event_detail='Detail 1',
            event_numset=2, event_location='Location 1', pcount=0,)

        event.person_set.create(fname='John', lname='Farmer')

        response = self.client.get('/1/')

        self.assertIn('John', response.content.decode())
        self.assertIn('Farmer', response.content.decode())


    def test_can_save_a_POST_request(self):
        event = Event.objects.create(event_name='Event 1', event_detail='Detail 1',
            event_numset=2, event_location='Location 1', pcount=0,)

        self.client.post('/1/', data={'firstname': 'firstname' , 'lastname': 'lastname'})

        self.assertEqual(event.person_set.count(), 1)
        new_person = event.person_set.first()
        self.assertEqual(new_person.fname, 'firstname')
        self.assertEqual(new_person.lname, 'lastname')

    def test_redirects_after_POST(self):
        event = Event.objects.create(event_name='Event 1', event_detail='Detail 1',
            event_numset=2, event_location='Location 1', pcount=0,)

        response = self.client.post('/1/', data={'firstname': 'firstname' , 'lastname': 'lastname'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/1/')

    def test_only_saves_items_when_necessary(self):
        self.client.get('/1/')
        self.assertEqual(Event.objects.count(), 0)



class EventModelTest(TestCase):

    def test_saving_and_retrieving_event(self):

        event = Event.objects.create(event_name='Event 1', event_detail='Detail 1',
            event_numset=2, event_location='Location 1', pcount=0,)

        saved_event = Event.objects.all()
        self.assertEqual(saved_event.count(), 1)
        
        name = saved_event[0]
        self.assertEqual(name.event_name, 'Event 1')
        
        person1 = event.person_set.create(fname='John', lname='Farmer')
        person1.save()

        person2 = event.person_set.create(fname='Gaben', lname='L')
        person2.save()

        saved_person = Person.objects.all()
        self.assertEqual(saved_person.count(), 2)

        first_person = saved_person[0]
        second_person = saved_person[1]
        self.assertEqual(first_person.fname, 'John')
        self.assertEqual(first_person.lname, 'Farmer')
        self.assertEqual(second_person.fname, 'Gaben')
        self.assertEqual(second_person.lname, 'L')