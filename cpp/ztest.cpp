#include <iostream>  
#include <Python.h>  

using namespace std;  

void os_type();
void Add();  
void TestTransferDict();  
void TestClass();  

int main()  
{  
    cout << "Starting Test..." << endl;  

    cout << "HelloWorld()-------------" << endl;  
    os_type();  

    cout << "Add()--------------------" << endl;  
    Add();  

    cout << "TestDict-----------------" << endl;  
    TestTransferDict();  
    cout << "TestClass----------------" << endl;  
    TestClass();  

    return 0;  
}  

//调用输出"Hello World"函数  
void os_type()  
{  
    PyObject * pModule = NULL;  
    PyObject * pFunc = NULL; 

    Py_Initialize(); 
    if (!Py_IsInitialized()) {
        cout << "Py_IsInitialized failed" << endl;
        return;
    }

    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append('./')");

    pModule =PyImport_ImportModule("Test");

    pFunc= PyObject_GetAttrString(pModule, "os_type");
    PyEval_CallObject(pFunc, NULL);
    Py_Finalize();
}

void Add() {
    Py_Initialize();
    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append('./')");

    PyObject *pModule, *pFunc;
    pModule = PyImport_ImportModule("Test");
    pFunc = PyObject_GetAttrString(pModule, "add");

    PyObject* pArgs = PyTuple_New(2);
    PyTuple_SetItem(pArgs, 0, Py_BuildValue("i", 5));
    PyTuple_SetItem(pArgs, 1, Py_BuildValue("i", 7));

    PyObject* pReturn = PyEval_CallObject(pFunc, pArgs);

    int result;
    PyArg_Parse(pReturn, "i", &result);
    cout << "5 + 7 = " << result << endl;

    Py_Finalize();
}
void TestTransferDict()  
{  
    Py_Initialize();  
    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append('./')");

    PyObject * pModule = NULL;      
    PyObject * pFunc = NULL;        
    pModule =PyImport_ImportModule("Test");
    pFunc= PyObject_GetAttrString(pModule, "TestDict"); 

    PyObject *pArgs = PyTuple_New(1);   
    PyObject *pDict = PyDict_New(); 
    PyDict_SetItemString(pDict, "Name", Py_BuildValue("s", "WangYao")); 
    PyDict_SetItemString(pDict, "Age", Py_BuildValue("i", 25)); 
    PyTuple_SetItem(pArgs, 0, pDict);

    PyObject *pReturn = NULL;  
    pReturn = PyEval_CallObject(pFunc, pArgs); 

    int size = PyDict_Size(pReturn);  
    cout << "返回字典的大小为: " << size << endl;  
    PyObject *pNewAge = PyDict_GetItemString(pReturn, "Age");  
    int newAge;  
    PyArg_Parse(pNewAge, "i", &newAge);  
    cout << "True Age: " << newAge << endl;  

    Py_Finalize();                  
}  


void TestClass()  
{  
    Py_Initialize();  
    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append('./')");

    PyObject * pModule = NULL;      
    pModule =PyImport_ImportModule("Test");

    PyObject *pClassPerson = PyObject_GetAttrString(pModule, "Person");  

    PyObject *pInstancePerson = PyInstance_New(pClassPerson, NULL, NULL);  

    PyObject_CallMethod(pInstancePerson, "greet", "s", "Hello Kitty");

    Py_Finalize();            
}
