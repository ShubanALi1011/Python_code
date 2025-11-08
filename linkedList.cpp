//#include <bits/stdc++.h>
#include <iostream>
using namespace std;
class Node{
    public:
        int data;
        Node* next;

        Node(int data){
            this->data = data;
            this->next = NULL;
        }
};
class LinkedList{
    private:
        Node* head;
        Node* tail;
    public:
        LinkedList(){
            head = NULL;
            tail = NULL;
        }

        void insertAtHead(int data){
            Node* temp = new Node(data);
            if(head == NULL){
                head = temp;
                tail = temp;
                return;
            }
            temp->next = head;
            head = temp;
        }
        void insertAtTail(int data){
            Node* temp = new Node(data);
            if(head == NULL){
                head = temp;
                tail = temp;
                return;
            }
            tail->next = temp;
            tail = temp;
        }

        void insertAtPos(int pos, int data){
            if(pos == 1){
                insertAtHead(data);
                return;
            }
            Node* temp = new Node(data);
            Node* curr = head;
            int cnt = 1;
            while(curr != NULL && cnt < pos-1){
                if(cnt == pos){
                    Node* forward = curr->next;
                    curr->next = temp;
                    temp->next = forward;
                }
                curr = curr->next;
                cnt++;
            }
        }

        void print(){
            Node* curr = head;
            while(curr != NULL){
                cout<<curr->data<<" -> ";
                curr = curr->next;
            }
            cout<<"NULL";
            cout<<endl;
        }
};
int main() {
    LinkedList root;
    root.insertAtHead(10);
    root.insertAtHead(5);
    root.insertAtHead(1);
    root.insertAtTail(20);
    root.insertAtPos(2,100);
    root.print();
    return 0;
}