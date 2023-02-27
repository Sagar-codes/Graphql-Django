import graphene
from graphene_django import DjangoObjectType, DjangoListField
from .models import *
from graphql import GraphQLError as ResolveInfo


"""Graphql - Attributes

    query
    mutation
    subscription
    fragment

"""


class CategoryType(DjangoObjectType):
    class Meta:
        model=Category
        fields = ("id", "name")

class QuizzesType(DjangoObjectType):
    class Meta:
        model=Quizzes
        fields = ("id", "title","category")

class QuestionType(DjangoObjectType):
    class Meta:
        model=Questions
        fields = ("id","title", "quiz")

class AnswerType(DjangoObjectType):
    class Meta:
        model=Answers
        fields = ("question", "answer_text")

class Query(graphene.ObjectType):
    # If we Use DjangoListField then we dont have to Add Resolver Function for query.

    quiz = graphene.String()
    """
    query{
        quiz
    }
    """
    def resolve_quiz(root, info):
        return f"This is First Question"

    all_quizzes = DjangoListField(QuizzesType)  # or we can use = graphene.List(QuizzesType)
    all_questions = graphene.List(QuestionType)

    def resolve_all_questions(root, info):
        return Questions.objects.all()   # filter(id=1)
    """
    query{
        allQuizzes{
            id,
            title
        }
        allQuestions{
            title,
            quiz {
            id
            }
        }
    }
    """

    def resolve_all_quizzes(root, info):
        return Quizzes.objects.all()   # filter(id=1)

# Getting single Data
    quizzById = graphene.Field(QuizzesType, id=graphene.Int())
    questionById = graphene.Field(QuestionType, id=graphene.Int())

    def resolve_quizzById(root, info, id):
        return Quizzes.objects.get(pk=id) 

    """
    query{
        quizzById(id:1){
            id,
            title
        }
        questionById(id:1){,
            title,
            quiz{
                id,
                title
            }
        
        }
    }
    """
    def resolve_questionById(root, info, id):
        return Questions.objects.get(pk=id)


    #Graphene List Filter
    GetAnswersById = graphene.List(AnswerType, id=graphene.Int())
    """
    query{
        GetAnswersById(id:1){
            question{
                title
            }
            answerText
        }
    }

    OR

    query GetQuestions($id: Int = 1){ 
        questionById(id:1){
            title
        }
        GetAnswersById(id:1){
            answerText
        }
    }

    -> GetQuestions($id: Int = 1) its a variable defined in the top to use
    -> questionById(id:$id){
            title
        }
    """

    def resolve_GetAnswersById(root, info, id):
        return Answers.objects.filter(question=id) # Note We cannot use get() here Cz We are Fteching the answers by list of graphene lib.



# CRUD USING GRAPHQL USING MUTATIONS

# Category

class AddCategoryMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name):
        category = Category(name=name) #model
        category.save()
        return AddCategoryMutation(category=category)

    """
    mutation firstMutation{
        addCategory(name:"JavaScript"){
            category{
                name
            }
        }
    }
    """

class updateCategoryMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name, id):
        category = Category.objects.get(id=id) #model
        category.name = name
        category.save()
        return updateCategoryMutation(category=category)

    """
    mutation{
        updateCategory(id:1, name:"React"){
            category{
                name
            }
        }
    }
    """

class DeleteCategoryMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id):
        category = Category.objects.get(id=id) #model
        category.delete()
        return "Category Deleted SUccessFully"

    """
    mutation{
        deleteCategory(id:1){
            category{
                id
            }
        }
    }
    """

# Quizzes
class CreateQuizMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        category_id = graphene.ID() 

    quiz = graphene.Field(QuizzesType)

    @classmethod
    def mutate(cls, root, info, title, category_id):
        category = Category.objects.filter(id=category_id).exists()
        if category:
            # raise ResolveInfo("No Category Found! Please Add Some .") 
            quiz = Quizzes(title=title, category_id=category_id) #model 
            #-> If we are not adding category object in model we need  category_id=category_id field and 
            # #->if we are adding category object we need to specify category=the_object
            quiz.save()
            return CreateQuizMutation(quiz=quiz)
        else:
            return Exception("No Category Found! Please Add Some .") 

    """
    mutation{
        createQuiz(title:"TypeScript Quiz", categoryId:4){
            quiz{
                title,
            }
        }
    }
    """

class updateQuizMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        title = graphene.String(required=True)
        category_id = graphene.ID() 

    quiz = graphene.Field(QuizzesType)

    @classmethod
    def mutate(cls, root, info, title, category_id, id):
        category = Category.objects.filter(id=category_id).exists()
        if category:
            # raise ResolveInfo("No Category Found! Please Add Some .") 
            quiz = Quizzes.objects.get(id=id)
            quiz.title=title
            quiz.category_id=category_id #model 
            #-> If we are not adding category object in model we need  category_id=category_id field and 
            # #->if we are adding category object we need to specify category=the_object
            quiz.save()
            return updateQuizMutation(quiz=quiz)
        else:
            return Exception("No Category Found! Please Add Some .")

    """
    mutation{
        updateQuiz(id:5, title:"Vanila Javascript", categoryId:4){
            quiz{
                title,
                category{
                    name
                }
            }
        }
    }
    """



class Mutation(graphene.ObjectType):

    add_category = AddCategoryMutation.Field()
    update_category = updateCategoryMutation.Field()
    delete_category = DeleteCategoryMutation.Field()

    createQuiz = CreateQuizMutation.Field()
    updateQuiz = updateQuizMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)